
__version__ = "0.0.1"

from napari_spatial_statistics._sample_data import make_random_points, make_2ch_non_random_points
from napari_spatial_statistics._spatial_statistics import neighborhood_enrichment_test
from napari_spatial_statistics._plot_widget import PlotWidget

from napari_spatial_statistics._neighborhood import distance_ckdtree, \
    distance_squidpy,\
    knearest_ckdtree

from napari_plugin_engine import napari_hook_implementation


@napari_hook_implementation
def napari_experimental_provide_function():
    return [neighborhood_enrichment_test,
            make_random_points,
            make_2ch_non_random_points,
            PlotWidget,
            distance_ckdtree,
            distance_squidpy,
            knearest_ckdtree]
