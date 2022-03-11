"""
This module is an example of a barebones sample data provider for napari.

It implements the "sample data" specification.
see: https://napari.org/plugins/stable/guides.html#sample-data

Replace code below according to your needs.
"""
import numpy as np

from napari.types import LayerDataTuple, List

def make_random_points(n_points=100,
                       size:int = 100,
                       dim: int = 3,
                       number_of_layers:int = 2) -> List[LayerDataTuple]:

    colors = ['orange', 'blue', 'magenta', 'pink', 'red', 'green', 'yellow']

    data = [
        (size * np.random.random((n_points, dim)),
        {
            'name': f'Random Points_{idx}',
            'size': size/40,
            'edge_width': 0,
            'face_color': colors[idx % len(colors)]
         },
        'points')
        for idx in range(number_of_layers)]
    return data
