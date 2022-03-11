"""
This module is an example of a barebones sample data provider for napari.

It implements the "sample data" specification.
see: https://napari.org/plugins/stable/guides.html#sample-data

Replace code below according to your needs.
"""
import numpy as np

from napari.types import PointsData, LayerDataTuple

def make_random_points(n_points=40,
                       size:int = 1000,
                       dim: int = 3) -> PointsData:
  data = size * np.random.random((n_points, dim))
  return data
