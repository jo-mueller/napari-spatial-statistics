from napari_spatial_statistics import make_random_points,\
    make_non_random_points,\
    make_random_spots
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

def test_spot_generation(make_napari_viewer):

    viewer = make_napari_viewer()
    spots = make_random_spots(sigma=1.5)
    for k in range(len(spots)):
        viewer.add_image(spots[k][0], **spots[k][1])

def test_maxima_detection(make_napari_viewer):
    from napari_spatial_statistics import detect_maxima
    from napari_spatial_statistics import merge_points_layers
    viewer = make_napari_viewer()
    spots = make_random_spots(sigma=1.5)

    for k in range(len(spots)):
        viewer.add_image(spots[k][0], **spots[k][1])

    assert len(viewer.layers) == 2

    pts_0 = detect_maxima(viewer.layers[0])
    pts_1 = detect_maxima(viewer.layers[1])

    viewer.add_points(pts_0[0], **pts_0[1])
    viewer.add_points(pts_1[0], **pts_1[1])

    merged_points = merge_points_layers(viewer)
    viewer.add_points(merged_points[0], **merged_points[1])

def test_merging_points_layer(make_napari_viewer):
    from napari_spatial_statistics import merge_points_layers
    viewer = make_napari_viewer()

    pts1 = make_random_points(n_classes=1)
    pts2 = make_random_points(n_classes=1)

    viewer.add_points(pts1[0], **pts1[1])
    viewer.add_points(pts2[0], **pts2[1])

    merged_points = merge_points_layers(viewer)
    viewer.add_points(merged_points[0], **merged_points[1])


if __name__ == '__main__':
    import napari
    test_maxima_detection(napari.Viewer)
