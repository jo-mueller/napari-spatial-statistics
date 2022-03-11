"""
This module is an example of a barebones QWidget plugin for napari

It implements the Widget specification.
see: https://napari.org/plugins/stable/guides.html#widgets

Replace code below according to your needs.
"""
from magicgui import magic_factory

from napari.types import PointsData, ImageData


# from anndata import AnnData
# import squidpy as sq
# import pandas as pd

import numpy as np

def test(a:ImageData, b: ImageData) -> ImageData:
    return a + b

# @magic_factory
# def neighborhood_enrichment_test(points_1: PointsData,
#                                  points_2: PointsData):

#     assert len(points_1.shape) == len(points_2.shape)

#     ndims = len(points_1.shape)

#     _coordinates =  np.zeros((points_1.shape[0] + points_2.shape[0],
#                               ndims + 1))


#     _coordinates[:points_1.shape[0], :-1] = points_1
#     _coordinates[:points_1.shape[0], -1] = 1
    
#     _coordinates[-points_2.shape[0]:, :-1] = points_2
#     _coordinates[-points_2.shape[0]:, -1] = 2

#     adata = AnnData(_coordinates,
#                     obs = {'ID': pd.Categorical(_coordinates[:, -1])},
#                     obsm={"spatial3d": _coordinates[:, :-1]})

#     sq.gr.spatial_neighbors(adata, coord_type="generic", spatial_key="spatial3d")
#     sq.gr.nhood_enrichment(adata, cluster_key="ID")
    


# if __name__ == "__main__":


#     points_a = np.random.random((10, 2))
#     points_b = np.random.random((10, 2))

#     neighborhood_enrichment_test(points_a, points_b)
