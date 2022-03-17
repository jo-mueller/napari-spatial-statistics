import numpy as np

def tst_spatial_stats_nhe(make_napari_viewer):

    from napari_spatial_statistics._neighborhood import knearest_ckdtree
    from napari_spatial_statistics._sample_data import make_random_points
    from napari_spatial_statistics._spatial_statistics import neighborhood_enrichment_test

    viewer = make_napari_viewer()

    pts = make_random_points(spatial_size=100, n_classes=2)
    pts = knearest_ckdtree(pts, n_neighbors=5)
    neighborhood_enrichment_test(viewer, pts)

def tst_spatial_stats_nhe2(make_napari_viewer):

    from napari_spatial_statistics._neighborhood import distance_ckdtree
    from napari_spatial_statistics._sample_data import make_random_points
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

if __name__ == '__main__':
    import napari
    tst_spatial_stats_nhe2(napari.Viewer)
