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

def add_features(layer, key, data):
    if hasattr(layer, 'properties'):
        layer.properties[key] = data
    if hasattr(layer, 'features'):
        layer.features[key] = data

def get_features(layer, key=None):
    if hasattr(layer, 'properties'):
        if key is None:
            return layer.properties
        else:
            return layer.properties[key]
    if hasattr(layer, 'features'):
        if key is None:
            return layer.features
        else:
            return layer.features[key]

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

from qtpy.QtWidgets import QWidget,\
    QVBoxLayout,\
    QSizePolicy,\
    QPushButton,\
    QHBoxLayout,\
    QFileDialog

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib as mpl

COLOR='white'
mpl.rcParams['text.color'] = COLOR
mpl.rcParams['axes.labelcolor'] = COLOR
mpl.rcParams['xtick.color'] = COLOR
mpl.rcParams['ytick.color'] = COLOR

from napari_tools_menu import register_dock_widget

import numpy as np

class MplCanvas(FigureCanvas):
    """
    Defines the canvas of the matplotlib window
    From https://github.com/haesleinhuepf/napari-workflow-inspector/blob/main/src/napari_workflow_inspector/_dock_widget.py
    """
    def __init__(self):
        self.fig = Figure()                         # create figure
        self.axes = self.fig.add_subplot(111)       # create subplot

        self.axes.spines['bottom'].set_color('white')
        self.axes.spines['top'].set_color('white')
        self.axes.spines['left'].set_color('white')
        self.axes.spines['right'].set_color('white')
        self.fig.patch.set_facecolor('#262930')
        self.axes.set_facecolor('#262930')
        self.axes.grid(which='major', linestyle='--', color='white', alpha=0.6)
        self.axes.tick_params(axis='both', colors='white')

        FigureCanvas.__init__(self, self.fig)       # initialize canvas
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

class matplotlibWidget(QWidget):
    """
    The matplotlibWidget class based on QWidget
    """
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        # save canvas and toolbar
        self.canvas = MplCanvas()
        self.toolbar = NavigationToolbar(self.canvas, self)
        # set layout and add them to widget
        self.vbl = QVBoxLayout()
        self.vbl.addWidget(self.toolbar)
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)

@register_dock_widget(menu="Visualization > Spatial statistics plot widget")
class PlotWidget(QWidget):
    def __init__(self, napari_viewer):
        super().__init__()
        self._viewer = napari_viewer

        self.plotwidget = matplotlibWidget()
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.plotwidget)

        self.ExportCSVButton = QPushButton('Export to csv')
        self.ExportPNGButton = QPushButton('Save as png')

        # widget for data export
        data_export_container = QWidget()
        data_export_container.setLayout(QHBoxLayout())
        data_export_container.layout().addWidget(self.ExportCSVButton)
        data_export_container.layout().addWidget(self.ExportPNGButton)
        self.layout().addWidget(data_export_container)

        self.df = None

        # connect buttons
        self.ExportPNGButton.clicked.connect(self.export_png)
        self.ExportCSVButton.clicked.connect(self.export_csv)

    def plot_from_dataframe(self, df, xkey = None, ykey = None, **kwargs):

        self.df = df
        self.plotwidget.canvas.axes.clear()

        if xkey is None:
            x = np.arange(0, len(df), 1)
        else:
            x = df[xkey].to_numpy()

        if ykey is None:
            ykey = df.columns.to_list()
            ykey.remove(xkey)
            y = df[ykey].to_numpy()
        else:
            y = df[ykey].to_numpy()

        for iy in range(len(ykey)):
            self.plotwidget.canvas.axes.plot(x, y[:, iy], label = ykey[iy])

        self.plotwidget.canvas.axes.set(**kwargs)
        self._postprocess()
        self.plotwidget.canvas.draw()


    def export_png(self):
        filename, _ = QFileDialog.getSaveFileName(caption='Save figure to file',
                                                  filter='*.png')
        if not filename.endswith('.csv'):
            filename += '.png'
        self.plotwidget.canvas.axes.figure.savefig(filename, dpi=150)

    def export_csv(self):
        filename, _ = QFileDialog.getSaveFileName(caption='Save data to file',
                                                  filter='*.csv')
        if not filename.endswith('.csv'):
            filename += '.csv'
        self.df.to_csv(filename)

    def _postprocess(self):
        self.plotwidget.canvas.axes.legend()
        self.plotwidget.canvas.axes.xaxis.label.set_color('white')
        self.plotwidget.canvas.axes.yaxis.label.set_color('white')

        self.plotwidget.canvas.axes.grid(which='major', linestyle='--',
                                         color='white', alpha=0.7)
