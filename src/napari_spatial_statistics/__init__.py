
__version__ = "0.0.1"

from ._sample_data import make_random_points,\
    make_random_spots,\
    brain_section
from ._spatial_statistics import nhe_test_widget,\
    density_map,\
    neighborhood_enrichment_test
from ._detect_maxima import detect_maxima,\
    merge_points_layers,\
    labels_to_points

from ._neighborhood import distance_ckdtree, distance_squidpy,\
    knearest_ckdtree

from napari_plugin_engine import napari_hook_implementation

@napari_hook_implementation
def napari_experimental_provide_function():
    return [make_random_points,
            make_random_spots,
            brain_section,
            distance_ckdtree,
            distance_squidpy,
            knearest_ckdtree,
            detect_maxima,
            merge_points_layers,
            density_map]

@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    return [nhe_test_widget]
