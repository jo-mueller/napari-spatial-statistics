import numpy as np

def test_utils():

    from napari_spatial_statistics._utils import adjacency_matrix_to_list_of_neighbors, \
        list_of_neighbors_to_adjacency_matrix
    adj_matrix = np.array([[1, 1, 0],
                           [1, 1, 1],
                           [0, 1, 1]])

    lst = adjacency_matrix_to_list_of_neighbors(adj_matrix)

    _adj_matrix = list_of_neighbors_to_adjacency_matrix(lst)

    assert np.array_equal(adj_matrix, _adj_matrix)

def test_utils2(make_napari_viewer):
    from napari_spatial_statistics._sample_data import make_random_points
    from napari_spatial_statistics._utils import get_features, add_features

    viewer = make_napari_viewer()

    n_points = 1000
    pts = make_random_points(n_classes=3, n_points=n_points)
    pts = viewer.add_points(pts[0], **pts[1])

    props = get_features(pts)
    assert 'Cell type' in list(props.keys())

    new_feature = ['test'] * n_points
    add_features(pts, 'new_cool_feature', new_feature)
    props = get_features(pts)

    assert 'new_cool_feature' in list(props.keys())


if __name__ == "__main__":
    import napari
    test_utils2(napari.Viewer)
