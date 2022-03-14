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


if __name__ == "__main__":
    test_utils()
