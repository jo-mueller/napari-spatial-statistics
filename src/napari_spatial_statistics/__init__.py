
__version__ = "0.0.1"

from napari_spatial_statistics._sample_data import make_random_points
from napari_spatial_statistics._spatial_statistics import neighborhood_enrichment_test
from napari_spatial_statistics._plot_widget import PlotWidget

from napari_plugin_engine import napari_hook_implementation


@napari_hook_implementation
def napari_experimental_provide_function():
    return [neighborhood_enrichment_test,
            make_random_points,
            PlotWidget]


if __name__ == '__main__':

    import napari
    viewer = napari.Viewer()

    pts = make_random_points()
    viewer.add_points(pts[0], **pts[1])
