"""
This module is an example of a barebones sample data provider for napari.

It implements the "sample data" specification.
see: https://napari.org/plugins/stable/guides.html#sample-data

Replace code below according to your needs.
"""
import numpy as np

from napari.types import LayerDataTuple, List


colors = np.array(['orange', 'blue', 'magenta', 'pink', 'red', 'green', 'yellow'])

def make_random_points(n_points: int = 1000,
                        n_classes: int = 3,
                        spatial_size: int = 100,
                        dim: int = 3) -> List[LayerDataTuple]:

    data = spatial_size * np.random.random((n_points, dim))
    point_type = np.random.randint(0, n_classes, size=n_points)

    properties = {'Cell type': point_type, 'Label': np.arange(0, n_points, 1)}
    props = {'name': 'Random points',
             'face_color': colors[point_type],
             'edge_width': 0,
             'properties': properties,
             'size': spatial_size/40}

    return (data, props, 'points')

def make_2ch_non_random_points(n_points: int = 1000,
                               spatial_size: int = 100,
                               sigma: float = 2,
                               dim: int = 3) -> List[LayerDataTuple]:

    data_ch1 = spatial_size * np.random.random((n_points, dim))
    noise = np.random.normal(scale=sigma, size=data_ch1.shape)

    data_ch2 = data_ch1 + noise

    point_type = np.array([np.zeros(n_points, dtype=int),
                           np.ones(n_points, dtype=int)]).flatten()
    data = np.vstack([data_ch1, data_ch2])

    properties = {'Cell type': point_type, 'Label': np.arange(0, n_points, 1)}
    props = {'name': 'Random points',
             'face_color': colors[point_type],
             'edge_width': 0,
             'properties': properties,
             'size': spatial_size/40}

    return (data, props, 'points')
