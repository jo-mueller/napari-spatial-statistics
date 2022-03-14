import numpy as np

def adjacency_matrix_to_list_of_neighbors(adj_matrix: np.ndarray):

    assert adj_matrix.shape[0] == adj_matrix.shape[1]

    list_of_neighbors = []
    for k in range(adj_matrix.shape[0]):
        list_of_neighbors.append(list(np.argwhere(adj_matrix[k] != 0).flatten()))

    return list_of_neighbors

def list_of_neighbors_to_adjacency_matrix(list_of_neighbors: list):

    adj_matrix = np.zeros([len(list_of_neighbors)] * 2, dtype=int)

    for k, entry in enumerate(list_of_neighbors):
        adj_matrix[k][np.array(entry)] = 1

    return adj_matrix

def set_features(layer, tabular_data):
    if hasattr(layer, "properties"):
        layer.properties = tabular_data
    if hasattr(layer, "features"):
        layer.features = tabular_data
