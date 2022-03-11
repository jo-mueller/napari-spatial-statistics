"""
This module is an example of a barebones sample data provider for napari.

It implements the "sample data" specification.
see: https://napari.org/plugins/stable/guides.html#sample-data

Replace code below according to your needs.
"""
import numpy as np

from napari.types import LayerDataTuple, List

def make_random_points(n_points: int = 1000,
                        n_classes: int = 3,
                        spatial_size: int = 100,
                        dim: int = 3) -> List[LayerDataTuple]:

    data = spatial_size * np.random.random((n_points, dim))
    point_type = np.random.randint(0, n_classes, size=n_points)

    colors = np.array(['orange', 'blue', 'magenta', 'pink', 'red', 'green', 'yellow'])

    properties = {'Cell type': point_type}
    props = {'name': 'Random points',
             'face_color': colors[point_type],
             'edge_width': 0,
             'properties': properties,
             'size': spatial_size/40}


    return (data, props, 'points')
