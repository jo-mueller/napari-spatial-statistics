
__version__ = "0.0.1"

from napari_spatial_statistics._sample_data import make_random_points 
from napari_spatial_statistics._spatial_statistics import test

from napari_plugin_engine import napari_hook_implementation


@napari_hook_implementation
def napari_experimental_provide_function():
    return [test, make_random_points]

if __name__ == "__main__":
    import napari
    viewer = napari.Viewer()
    pts = make_random_points()
    pts1 = make_random_points()
    viewer.add_points(pts, face_color='orange')
    viewer.add_points(pts1, face_color='blue')
    
    # napari.layers._layer_actions._duplicate_layer(viewer.layers)
    # pts = make_random_points()
