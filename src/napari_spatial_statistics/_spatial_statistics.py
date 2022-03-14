"""
This module is an example of a barebones QWidget plugin for napari

It implements the Widget specification.
see: https://napari.org/plugins/stable/guides.html#widgets

Replace code below according to your needs.
"""
from napari.layers import Points

from anndata import AnnData
import squidpy as sq
import pandas as pd
from scipy import sparse

from napari_tools_menu import register_dock_widget

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import napari.types
    import napari.viewer


@register_dock_widget(menu="Measurement > Spatial statistics (squidpy, nss)")
def neighborhood_enrichment_test(viewer: 'napari.viewer.Viewer',
                                 points: Points,
                                 n_permutations=1000):

    from napari_spatial_statistics._utils import list_of_neighbors_to_adjacency_matrix

    neighbors = points.properties['neighbors']
    _neighbors = [None] * len(neighbors)
    for idx, entry in enumerate(neighbors):
        _neighbors[idx] = [int(i) for i in entry.split(',')]

    adj_matrix = list_of_neighbors_to_adjacency_matrix(_neighbors)
    adj_matrix = sparse.csr_matrix(adj_matrix)


    adata = AnnData(points.data,
                    obs = {'Cell type': pd.Categorical(points.properties['Cell type'])},
                    obsp = {'spatial_connectivities': adj_matrix},
                    obsm={"spatial3d": points.data})

    result = sq.gr.nhood_enrichment(adata, cluster_key="Cell type",
                                    n_perms=n_permutations,
                                    show_progress_bar=False,
                                    n_jobs=-1, copy=True)
    print(result)
