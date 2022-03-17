import numpy as np
from napari_skimage_regionprops._table import add_table, TableWidget

from napari.types import PointsData
from napari.layers import Points, Layer

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import napari.viewer

def properties_to_table(viewer: 'napari.viewer.Viewer',
                        points: Points):

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
