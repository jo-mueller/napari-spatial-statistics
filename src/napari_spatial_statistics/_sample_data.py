"""
This module is an example of a barebones sample data provider for napari.

It implements the "sample data" specification.
see: https://napari.org/plugins/stable/guides.html#sample-data

Replace code below according to your needs.
"""
import numpy as np

from napari.types import LayerDataTuple, List


img_colors = np.array(['bop orange', 'bop blue', 'magenta', 'pink', 'red', 'green', 'yellow'])
pt_colors = np.array(['orange', 'blue', 'magenta', 'pink', 'red', 'green', 'yellow'])

def make_random_spots(n_spots: int = 1000,
                      n_classes: int = 2,
                      spatial_size: int = 100,
                      sigma: float = 2,
                      dim: int = 3) -> List[LayerDataTuple]:
    from skimage import filters

    images = []

    for idx in range(n_classes):
        image = np.zeros(spatial_size**dim, dtype=float)
        locations = np.random.randint(0, spatial_size**dim, size=n_spots)
        image[locations] = 1
        image = np.reshape(image, newshape=([spatial_size] * dim))
        image = filters.gaussian(image, sigma)
        image = image/image.max()
        images.append((image,
                       {'name': f'Marker {idx}',
                        'colormap': img_colors[idx]},
                       'image'))

    return images

def make_random_points(n_points: int = 1000,
                        n_classes: int = 3,
                        spatial_size: int = 100,
                        dim: int = 3) -> List[LayerDataTuple]:

    data = spatial_size * np.random.random((n_points, dim))
    point_type = np.random.randint(0, n_classes, size=n_points)

    properties = {'Label': np.arange(0, n_points, 1), 'Cell type': point_type}
    props = {'name': 'Random points',
             'face_color': pt_colors[point_type],
             'edge_width': 0,
             'properties': properties,
             'size': spatial_size/40}

    return (data, props, 'points')

def make_non_random_points(n_points: int = 1000,
                           n_classes: int = 3,
                           spatial_size: int = 100,
                           sigma: float = 2,
                           dim: int = 3) -> List[LayerDataTuple]:

    pts_per_channel = n_points//n_classes
    data_chx = []

    for idx in range(n_classes):
        if len(data_chx) == 0:
            data_chx.append(
                spatial_size * np.random.random((pts_per_channel, dim))
                )
        else:
            noise = np.random.normal(scale=sigma, size=data_chx[0].shape)
            data_chx.append(
                data_chx[idx-1] + noise
                )

    data = np.vstack(data_chx)
    point_type = np.array([[i]*pts_per_channel for i in range(n_classes)]).flatten()

    properties = {'Label': np.arange(0, pts_per_channel*n_classes, 1),
                  'Cell type': point_type}
    props = {'name': 'Random points',
             'face_color': pt_colors[point_type],
             'edge_width': 0,
             'properties': properties,
             'size': spatial_size/40}

    return (data, props, 'points')
