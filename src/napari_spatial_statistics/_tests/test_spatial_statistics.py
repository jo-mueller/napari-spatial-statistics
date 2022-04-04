import numpy as np
from napari_spatial_statistics import make_random_points,\
    make_non_random_points,\
    make_random_spots

def tst_spatial_stats_nhe(make_napari_viewer):

    from napari_spatial_statistics._neighborhood import knearest_ckdtree
    from napari_spatial_statistics._spatial_statistics import neighborhood_enrichment_test

    viewer = make_napari_viewer()

    pts = make_random_points(spatial_size=100, n_classes=2)
    pts = knearest_ckdtree(pts, n_neighbors=5)
    neighborhood_enrichment_test(viewer, pts)

def tst_spatial_stats_nhe2(make_napari_viewer):

    from napari_spatial_statistics._neighborhood import distance_ckdtree
    from napari_spatial_statistics._spatial_statistics import neighborhood_enrichment_test

    viewer = make_napari_viewer()

    n_classes = 2
    pts = make_random_points(spatial_size=100, n_classes=n_classes)
    pts = viewer.add_points(pts[0], **pts[1])
    distance_ckdtree(pts, radius=10, show_neighborhood=False)

    pts = viewer.layers[0]
    result = neighborhood_enrichment_test(pts.data, pts.properties, on_feature='Cell type')

    assert 'zscore' in list(result.keys()) and 'count' in list(result.keys())
    assert np.array_equal(result['zscore'].shape, np.array([n_classes, n_classes]))

def test_spatial_stats3(make_napari_viewer):
    from napari_spatial_statistics._neighborhood import knearest_ckdtree
    from napari_spatial_statistics._spatial_statistics import nhe_test_widget, neighborhood_enrichment_test
    from napari_spatial_statistics._plot_widget import PlotWidget
    from scipy.spatial import cKDTree
    from napari_spatial_statistics._utils import set_features

    viewer = make_napari_viewer()
    widget = nhe_test_widget(viewer)
    plt_widget = PlotWidget(viewer)

    viewer.window.add_dock_widget(widget)
    viewer.window.add_dock_widget(plt_widget)

    # add some data
    pts = make_non_random_points()
    pts_layer = viewer.add_points(pts[0], **pts[1])

    # Calc neighborhood
    tree = cKDTree(pts_layer.data)
    neighbors = tree.query(list(pts_layer.data), k=10)

    #TODO: Find a nicer way to store list(s) of neighbors
    # Really dirty hack: napari does not allow property entries to be a list of
    # multiple items. Hence, we convert the list of neighbors to a string and
    # put it to the properties.
    neighbors_str = [",".join(map(str, neighbors[1][i])) for i in range(len(neighbors[1]))]
    pts_layer.properties['neighbors'] = neighbors_str
    set_features(pts_layer, pts_layer.properties)

    neighborhood_enrichment_test(pts_layer.data, pts_layer.properties, on_feature='Cell type',
                                 n_permutations=100, ax=plt_widget.plotwidget.canvas.axes)


if __name__ == '__main__':
    import napari
    test_spatial_stats3(napari.Viewer)
