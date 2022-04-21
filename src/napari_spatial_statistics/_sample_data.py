"""
This module is an example of a barebones sample data provider for napari.

It implements the "sample data" specification.
see: https://napari.org/plugins/stable/guides.html#sample-data

Replace code below according to your needs.
"""
import numpy as np

from napari.types import LayerDataTuple, List, ImageData


img_colors = np.array(['bop orange', 'bop blue', 'magenta', 'pink', 'red', 'green', 'yellow'])
pt_colors = np.array(['orange', 'blue', 'magenta', 'pink', 'red', 'green', 'yellow'])

def brain_section() -> ImageData:
    import os
    import pathlib
    from skimage import io

    parent = pathlib.Path(__file__).parent.resolve()
    filename = os.path.join(parent, '..', '..', 'docs', 'data', 'DAPI.png')
    image = io.imread(filename)

    return image

def make_random_spots(n_spots: int = 1000,
                      n_classes: int = 2,
                      spatial_size: int = 100,
                      randomness: float = 10,
                      sigma: float = 2,
                      dim: int = 3) -> List[LayerDataTuple]:
    from skimage import filters

    positions = make_random_points(n_points=n_spots, n_classes=n_classes,
                                   spatial_size=spatial_size,
                                   randomness=randomness,
                                   dim=dim)

    # Turn spots into images
    images = [None] * n_classes
    offset = abs(np.min(positions[0], axis=0).flatten().astype(int))
    dimensions = np.max(positions[0], axis=0).flatten().astype(int) +\
        offset + 1

    for idx in range(n_classes):
        image = np.zeros(dimensions)
        props = positions[1]['properties']
        locations = positions[0][props['Cell type'] == idx].astype(int) +\
            offset[None, :]

        image[[locations[:, i] for i in range(locations.shape[1])]] = 1
        image = filters.gaussian(image, sigma) * 1000

        images[idx] = (image,
                      {'name': f'Marker {idx}',
                      'colormap': img_colors[idx]},
                      'image')

    return images

def make_random_points(n_points: int = 1000,
                       n_classes: int = 3,
                       spatial_size: int = 100,
                       randomness: float = 2,
                       dim: int = 3) -> List[LayerDataTuple]:
    """
    Create random points layer data.

    This function will create a points layer with `n_classes` different object
    types, which is stored in `layer.properties`. On creation, all point types
    have the same position, making them highly spatially co-localized. A set
    amount of noise can be added to the positions to make the object types'
    locations more independent of each other.
    """

    pts_per_channel = n_points//n_classes
    data_chx = []

    for idx in range(n_classes):
        if len(data_chx) == 0:
            data_chx.append(
                spatial_size * np.random.random((pts_per_channel, dim))
                )
        else:
            noise = np.random.normal(scale=randomness, size=data_chx[0].shape)
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
