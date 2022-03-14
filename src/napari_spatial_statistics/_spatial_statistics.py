"""
This module is an example of a barebones QWidget plugin for napari

It implements the Widget specification.
see: https://napari.org/plugins/stable/guides.html#widgets

Replace code below according to your needs.
"""
import tqdm

from napari.types import PointsData
from napari.layers import Points

from anndata import AnnData
import squidpy as sq
import pandas as pd
import numpy as np
from scipy import sparse

from napari_tools_menu import register_dock_widget
import warnings

from typing import TYPE_CHECKING
from enum import Enum
if TYPE_CHECKING:
    import napari.types
    import napari.viewer


from ._plot_widget import PlotWidget

class spatial_statistics_method(Enum):
    ripley_function = 0
    newman_assortativity = 1
    centrality_score = 2
    cluster_cooccurrence = 3
    neighborhood_enrichment_test = 4
    object_object_correlation = 5




# def spatial_statistics(viewer: 'napari.viewer.Viewer',
#                         points: PointsData,
#                         test_method: spatial_statistics_method):

#     if isinstance(test_method, spatial_statistics_method):
#         test_method = test_method.value

#     props = list(points[1]['properties'].keys())
#     if len(props) > 1 and test_method.value in [0, 1, 2]:
#         warnings.warn("Test is intended for single object type. All objects " +
#                       "will be considered as same type.")

#     # annotated_data = _create_neighborhood(points, nh_method)



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
