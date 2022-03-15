from enum import Enum
from typing import TYPE_CHECKING
from napari.layers import Points
from napari_tools_menu import register_dock_widget

if TYPE_CHECKING:
    import napari.types

from napari_spatial_statistics._utils import adjacency_matrix_to_list_of_neighbors,\
    set_features

@register_dock_widget(menu="Neighborhood > distance-neighborhood (scipy, nss)")
def distance_ckdtree(points: Points, radius: float = 1) -> Points:
    """Calculate neighborhood graph based on ckdtree distance.

    See also
    --------
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.cKDTree.html
    """

    from scipy.spatial import cKDTree

    if isinstance(points, tuple):
        points = Points(points[0], **points[1])

    tree = cKDTree(points.data)
    neighbors = tree.query_ball_point(points.data, r=radius)

    neighbors_str = [",".join(map(str, neighbors[i])) for i in range(len(neighbors))]
    points.properties['neighbors'] = neighbors_str
    set_features(points, points.properties)

    return points

@register_dock_widget(menu="Neighborhood > Delaunay-neighborhood (scipy, nss)")
def delaunay_scipy(points: Points) -> Points:
    """Calculate delaunay tesselation using scipy.

    See also
    --------
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.Delaunay.html
    """
    from scipy.spatial import Delaunay
    if isinstance(points, tuple):
        points = Points(points[0], **points[1])

    neighbors = Delaunay(points[0])

    # Convert to str format
    neighbors_str = [",".join(map(str, neighbors[i])) for i in range(len(neighbors))]
    points.properties['neighbors'] = neighbors_str
    set_features(points, points.properties)

    return points

@register_dock_widget(menu="Neighborhood > distance-neighborhood (squidpy, nss)")
def distance_squidpy(points: Points, radius: float) -> Points:
    """Calculate distance-based neighborhood graph with squidpy.
    
    See also
    --------
    https://squidpy.readthedocs.io/en/latest/auto_examples/graph/compute_spatial_neighbors.html
        
    """
    from anndata import AnnData
    import squidpy as sq

    if isinstance(points, tuple):
        points = Points(points[0], **points[1])

    adata = AnnData(points[0],obs = points[1]['properties'],
                    obsm={"spatial3d": points[0]})
    sq.gr.spatial_neighbors(adata, coord_type="generic",
                            spatial_key="spatial3d", radius=radius)

    # Convert result to correct format
    adj_matrix = adata.obsp['spatial_connectivities'].toarray()
    lst_of_neighbors = adjacency_matrix_to_list_of_neighbors(adj_matrix)

    points.properties['neighbors'] = [str(x)[1:-1] for x in list(lst_of_neighbors)]
    set_features(points, points.properties)

    return points

@register_dock_widget(menu="Neighborhood > k-nearest neighbors (scipy, nss)")
def knearest_ckdtree(points: Points, n_neighbors: int = 5) -> Points:
    """Calculate k-nearest neighborhood graph with scipy.

    See also
    --------
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.cKDTree.html

    """

    from scipy.spatial import cKDTree

    if isinstance(points, tuple):
        points = Points(points[0], **points[1])

    tree = cKDTree(points.data)
    neighbors = tree.query(list(points.data), k=n_neighbors)

    #TODO: Find a nicer way to store list(s) of neighbors
    # Really dirty hack: napari does not allow property entries to be a list of
    # multiple items. Hence, we convert the list of neighbors to a string and
    # put it to the properties.
    neighbors_str = [",".join(map(str, neighbors[1][i])) for i in range(len(neighbors[1]))]
    points.properties['neighbors'] = neighbors_str
    set_features(points, points.properties)

    return points
