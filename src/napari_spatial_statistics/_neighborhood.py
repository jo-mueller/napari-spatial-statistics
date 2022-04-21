from typing import TYPE_CHECKING

from napari.layers import Points
from napari_tools_menu import register_dock_widget
from ._utils import properties_to_table

if TYPE_CHECKING:
    import napari.types

from napari_spatial_statistics._utils import adjacency_matrix_to_list_of_neighbors,\
    add_features,\
    get_features

@register_dock_widget(menu="Neighborhood > distance-neighborhood (scipy, nss)")
def distance_ckdtree(points: Points,
                     radius: float = 1.0,
                     show_neighborhood: bool = True,
                     viewer: 'napari.viewer.Viewer' = None):

    from scipy.spatial import cKDTree

    if isinstance(points, tuple):
        points = Points(points[0], **points[1])

    tree = cKDTree(points.data)
    neighbors = tree.query_ball_point(points.data, r=radius)

    neighbors_str = [",".join(map(str, neighbors[i])) for i in range(len(neighbors))]
    add_features(points, 'neighbors', neighbors_str)

    if show_neighborhood and viewer is not None:
        properties_to_table(viewer, points)

    return get_features(points)

@register_dock_widget(menu="Neighborhood > distance-neighborhood (squidpy, nss)")
def distance_squidpy(points: Points,
                     radius: float = 1.0,
                     show_neighborhood: bool = True,
                     viewer: 'napari.viewer.Viewer' = None):
    from anndata import AnnData
    import squidpy as sq

    if isinstance(points, tuple):
        points = Points(points[0], **points[1])

    adata = AnnData(points.data,
                    obs = points.properties,
                    obsm={"spatial3d": points.data})
    sq.gr.spatial_neighbors(adata, coord_type="generic",
                            spatial_key="spatial3d", radius=radius)

    # Convert result to correct format
    adj_matrix = adata.obsp['spatial_connectivities'].toarray()
    lst_of_neighbors = adjacency_matrix_to_list_of_neighbors(adj_matrix)

    neighbors_str = [str(x)[1:-1] for x in list(lst_of_neighbors)]
    add_features(points, 'neighbors', neighbors_str)

    if show_neighborhood and viewer is not None:
        properties_to_table(viewer, points)

    return get_features(points)

@register_dock_widget(menu="Neighborhood > k-nearest neighbors (scipy, nss)")
def knearest_ckdtree(points: Points,
                     n_neighbors: int = 5,
                     show_neighborhood: bool = True,
                     viewer: 'napari.viewer.Viewer' = None):

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
    add_features(points, 'neighbors', neighbors_str)

    if show_neighborhood and viewer is not None:
        properties_to_table(viewer, points)

    return get_features(points)
