from napari_spatial_statistics import make_random_points

# add your tests here...


def test_point_generation(make_napari_viewer):
    viewer = make_napari_viewer()
    pts = make_random_points(n_points=200, number_of_layers=2)
    for pt in pts:
        viewer.add_points(pt[0], **pt[1])

    assert len(viewer.layers) == 2
