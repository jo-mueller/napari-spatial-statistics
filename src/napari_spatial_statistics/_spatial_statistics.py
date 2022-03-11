"""
This module is an example of a barebones QWidget plugin for napari

It implements the Widget specification.
see: https://napari.org/plugins/stable/guides.html#widgets

Replace code below according to your needs.
"""
import tqdm

from napari.types import PointsData

from anndata import AnnData
import squidpy as sq
import pandas as pd

import numpy as np
from napari_tools_menu import register_dock_widget

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import napari.types
    import napari.viewer

from ._plot_widget import PlotWidget

@register_dock_widget(menu="Measurement > Neighborhood enrichment test (squidpy, nss)")
def neighborhood_enrichment_test(viewer: 'napari.viewer.Viewer',
                                 points_1: PointsData,
                                 points_2: PointsData,
                                 max_radius: float = 100,
                                 sampling_rate: float = 1,
                                 n_permutations=100):

    # Make sure that both points layers have same dimension
    assert len(points_1.data.shape) == len(points_2.data.shape)

    # Make sure to have enough sampling points
    assert sampling_rate < max_radius/2.0


    coordinates = np.vstack([points_1.data, points_2.data])
    ID = np.vstack([[1] * points_1.data.shape[0],
                    [2] * points_2.data.shape[0]]).flatten()

    adata = AnnData(coordinates,
                    obs = {'ID': pd.Categorical(ID)},
                    obsm={"spatial3d": coordinates})

    radii = np.arange(sampling_rate, max_radius, sampling_rate, dtype=float)
    results = []

    for radius in tqdm.tqdm(radii):
        sq.gr.spatial_neighbors(adata, coord_type="generic",
                                spatial_key="spatial3d", radius=radius)
        results.append(sq.gr.nhood_enrichment(adata, cluster_key="ID",
                                              n_perms=n_permutations,
                                              show_progress_bar=False,
                                              n_jobs=-1, copy=True))

    # Reformat results to dataframe
    results = np.asarray(results)
    df = pd.DataFrame()
    df['distance'] = radii
    df[f'z_score {points_1.name} vs {points_2.name}'] = results[:, 0, 0, 1]

    if all(np.nanmax(np.abs(results)[:, 0], axis=0).flatten() < 5):
        ylim = [-5, 5]
    else:
        ylim = [None, None]

    widget = PlotWidget(viewer)
    widget.plot_from_dataframe(df, xkey='radius', ylim=ylim, xlabel='radius',
                               ylabel='Z-score [a.u.]')
    viewer.window.add_dock_widget(widget)
