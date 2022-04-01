import numpy as np
from napari_skimage_regionprops._table import add_table, TableWidget

from napari.layers import Points, Layer

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import napari.viewer


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


def properties_to_table(viewer: 'napari.viewer.Viewer',
                        points: Points):
    """Put properties of a points layer into a table widget."""

    # Convert to napari points layer
    if isinstance(points, tuple):
        points = Points(points[0], **points[1])

    tablewidget = add_table(points, viewer)

    tablewidget._view.clicked.connect(lambda: highlight_neighbors(viewer,
                                                                  points,
                                                                  tablewidget))

def highlight_neighbors(viewer: 'napari.viewer.Viewer',
                        layer: Layer,
                        table_widget: TableWidget):
    """Highlight neighbors of a selected point in a table widget."""

    row = int(table_widget._view.currentRow())
    neighbors = table_widget._table["neighbors"][row]
    neighbors = np.array([int(x) for x in neighbors.split(',')])  # convert to indices

    edgecolors = np.zeros((layer.data.shape[0], 4), dtype=float)
    edgewidth = np.zeros(layer.data.shape[0])
    edgecolors[:, -1] = 1  # set alpha to 1

    edgecolors[neighbors] = [0.75, 0.75, 0.75, 1]
    edgecolors[row] = [1, 1, 1, 1]
    edgewidth[neighbors] = 0.75
    edgewidth[row] = 0.75

    layer.edge_color = edgecolors
    layer.edge_width = edgewidth
