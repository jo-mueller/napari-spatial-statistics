from napari_spatial_statistics import make_random_points,\
    make_random_spots,\
    detect_maxima
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

    pts = make_random_points()
    viewer.add_points(pts[0], **pts[1])

    assert len(viewer.layers) == 1
    assert len(np.unique(pts[1]['properties']['Cell type'])) == 3

def test_spot_generation(make_napari_viewer):

    viewer = make_napari_viewer()
    spots = make_random_spots(sigma=1.5)
    for k in range(len(spots)):
        viewer.add_image(spots[k][0], **spots[k][1])
        detect_maxima(spots[k][0], threshold_value=0.1)

if __name__ =='__main__':
    import napari
    test_spot_generation(napari.Viewer)
