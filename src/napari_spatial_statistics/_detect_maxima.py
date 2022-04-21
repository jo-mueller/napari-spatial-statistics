# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 13:57:00 2022

@author: johamuel
"""

from napari_tools_menu import register_dock_widget
from napari.layers import Points
from napari.types import ImageData, LayerDataTuple, LabelsData, PointsData
import napari
import numpy as np

from skimage import feature

colors = np.array(['orange', 'blue', 'magenta', 'pink', 'red', 'green', 'yellow'])


@register_dock_widget(menu="Process > Labels to Points (nss)")
def labels_to_points(labels: LabelsData) -> PointsData:

    from skimage import measure
    props = measure.regionprops_table(labels, properties=['centroid'])
    data = np.asarray([props[key] for key in props.keys()]).T

    return data


@register_dock_widget(menu="Process > Merge point layers (nss)")
def merge_points_layers(viewer: napari.viewer.Viewer) -> LayerDataTuple:
    layers = viewer.layers

    layers_to_merge = []
    for lay in layers:
        if isinstance(lay, Points):
            layers_to_merge.append(lay)

    data = np.vstack([lay.data for lay in layers_to_merge])
    point_type = np.concatenate([[lay.name] * lay.data.shape[0] for lay in layers_to_merge]).flatten()
    label = np.arange(0, data.shape[0], 1)

    size = np.concatenate([lay.size for lay in layers_to_merge]).flatten().mean()

    face_colors = {lay.name: colors[idx] for idx, lay in enumerate(layers_to_merge)}

    properties = {'Point_type': point_type,
                  'Label': label}
    params = {'name': 'Fused point layer',
             'size': size,
             'edge_width': 0,
             'face_color': [face_colors[point] for point in point_type],
             'properties': properties}
    return (data, params, 'Points')

@register_dock_widget(menu="Process > Peak detection (scikit-image, nss)")
def detect_maxima(image: ImageData,
                  minimal_distance: int=10,
                  exclude_border: bool = True,
                  threshold_value: float = 100
                  ) -> PointsData:

    points = feature.peak_local_max(image,
                                    min_distance=minimal_distance,
                                    exclude_border=exclude_border,
                                    threshold_abs=threshold_value)
    return points
