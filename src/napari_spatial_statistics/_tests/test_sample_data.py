from napari_spatial_statistics import make_random_points, make_non_random_points
import numpy as np


def test_point_generation(make_napari_viewer):
    viewer = make_napari_viewer()

    n_classes = 3

    pts = make_random_points(n_classes=n_classes)
    viewer.add_points(pts[0], **pts[1])

    assert len(viewer.layers) == 1
    assert len(np.unique(pts[1]['properties']['Cell type'])) == n_classes

def test_correlated_data_generator(make_napari_viewer):

    viewer = make_napari_viewer()

    pts = make_non_random_points()
    viewer.add_points(pts[0], **pts[1])

    assert len(viewer.layers) == 1
    assert len(np.unique(pts[1]['properties']['Cell type'])) == 3

if __name__ == '__main__':
    import napari
    test_correlated_data_generator(napari.Viewer)
