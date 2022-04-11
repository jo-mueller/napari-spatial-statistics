from napari_spatial_statistics import make_random_points,\
    make_random_spots

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

def test_label_centroid_detection(make_napari_viewer):
    from napari_spatial_statistics import labels_to_points
    from skimage import measure, filters

    viewer = make_napari_viewer()

    pts1 = make_random_spots(n_classes=1, sigma=1.0)[0][0]
    viewer.add_image(pts1)
    binary = pts1 > filters.threshold_otsu(pts1)
    labels = measure.label(binary)

    viewer.add_labels(labels)

    centroids = labels_to_points(labels)
    viewer.add_points(centroids, size=2)


if __name__ == '__main__':
    import napari
    test_label_centroid_detection(napari.Viewer)
