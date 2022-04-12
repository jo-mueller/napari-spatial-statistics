"""
This module is an example of a barebones QWidget plugin for napari

It implements the Widget specification.
see: https://napari.org/plugins/stable/guides.html#widgets

Replace code below according to your needs.
"""
from anndata import AnnData
import squidpy as sq
import pandas as pd
from scipy import sparse

from pathlib import Path
import os

from qtpy.QtCore import QEvent, QObject
from qtpy import uic
from qtpy.QtWidgets import (
    QGridLayout,
    QSpinBox,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget
)
from magicgui.widgets import create_widget

from napari_tools_menu import register_dock_widget
from napari.layers import Points
from napari.types import PointsData, ImageData

from ._utils import PlotWidget, list_of_neighbors_to_adjacency_matrix


from typing import TYPE_CHECKING, Union
if TYPE_CHECKING:
    import napari.types


@register_dock_widget(menu="Measurement > Neighborhood enrichment test (squidpy, nss)")
class nhe_test_widget(QWidget):
    def __init__(self, napari_viewer):
        super().__init__()

        self.viewer = napari_viewer
        self.layer_select = create_widget(annotation=Points, label="points_layer")

        uic.loadUi(os.path.join(Path(__file__).parent, './nhe_test_widget.ui'), self)

        self.container_input.layout().addWidget(self.layer_select.native, 0, 1)
        self.installEventFilter(self)

        # Connect functions
        self.layer_select.changed.connect(self._update_props)
        self.layer_select.parent_changed.emit(self.parent())
        self.pushButton_run.clicked.connect(self._run)

    def _run(self):
        plt_widget = PlotWidget(self.viewer)

        selected_layer = self.layer_select.value
        neighborhood_enrichment_test(points=selected_layer.data,
                                     properties=selected_layer.properties,
                                     on_feature=self.property_select.currentText(),
                                     n_permutations=self.spinbox_n_permutations.value(),
                                     ax=plt_widget.plotwidget.canvas.axes)

        plt_widget.plotwidget.canvas.draw()
        self.viewer.window.add_dock_widget(plt_widget)

    def _update_props(self):
        try:
            layer = self.layer_select.value
            properties = [str(key) for key in layer.properties.keys()]
            self.property_select.clear()
            self.property_select.addItems(properties)
        except Exception:
            pass

    def eventFilter(self, obj: QObject, event: QEvent):
        # See https://forum.image.sc/t/composing-workflows-in-napari/61222/3
        if event.type() == QEvent.ParentChange:
            self.layer_select.parent_changed.emit(self.parent())

        return super().eventFilter(obj, event)


def neighborhood_enrichment_test(points: PointsData,
                                 properties: dict,
                                 on_feature: str,
                                 n_permutations=1000,
                                 ax = None):
    """
    Run neighborhood enrichment test on set of points.

    Uses squidpy to run a neighborhood enrichment test (NHET). For this,
    a feature (`on_feature`) needs to be selected that divides points into
    classes. The NHET enrichment test then checks whether these classes appear
    close to each other compared to random class distribution.

    *Note*: The passed points data must have a `.properties` atribute
    (type: dict) with a `neighbors` key.

    Parameters
    ----------
    points : Points
        napari points layer
    on_feature : str
        feature which should be used to assign a class to every point. Must be
        a key in the points.properties dict.
    n_permutations : TYPE, optional
        NHET shuffles the point classes and calculates neighborhood stats for
        every of the `n_permutations` repeats. The default is 1000.

    Returns
    -------
    tuple(z-score, counts)

    See also
    --------
    https://squidpy.readthedocs.io/en/latest/api/squidpy.pl.nhood_enrichment.html
    """
    assert 'neighbors' in list(properties.keys())

    neighbors = properties['neighbors']
    _neighbors = [None] * len(neighbors)
    for idx, entry in enumerate(neighbors):
        _neighbors[idx] = [int(i) for i in entry.split(',')]

    adj_matrix = list_of_neighbors_to_adjacency_matrix(_neighbors)
    adj_matrix = sparse.csr_matrix(adj_matrix)

    adata = AnnData(points,
                    obs = {on_feature: pd.Categorical(properties[on_feature])},
                    obsp = {'spatial_connectivities': adj_matrix},
                    obsm={"spatial3d": points.data},
                    dtype=points.dtype)

    sq.gr.nhood_enrichment(adata, cluster_key=on_feature)
    sq.pl.nhood_enrichment(adata, cluster_key=on_feature, ax=ax)

    return adata.uns[f'{on_feature}_nhood_enrichment']


@register_dock_widget(menu="Measurement > Density map (vedo, nss)")
def density_map(points: PointsData,
                radius:float = 50) -> ImageData:
    """
    Generate a density map from points data.

    Parameters
    ----------
    points : PointsData
    radius : float, optional
        The local neighborhood is specified as the radius around each sample
        position (each voxel). The default is None.
    computeGradient : bool, optional
        Turn on/off the generation of the gradient vector, gradient magnitude
        scalar, and function classification scalar. By default this is off.
        Note that this will increase execution time and the size of the output.
        The default is False.

    Returns
    -------
    ImageData

    See also
    --------
    https://vedo.embl.es/autodocs/content/vedo/pointcloud.html


    """
    import vedo
    import numpy as np
    pointcloud = vedo.pointcloud.Points(points)
    vol = pointcloud.density(radius=radius,
                             dims=np.max(points, axis=0).astype(int))
    ndims = points.shape[1]

    # Somehow vedo returns a 3D volume with XYZ for 2D data
    if ndims == 2:
        vol = vol.tonumpy()[..., 0]
    else:
        vol = vol.tonumpy()

    return vol
