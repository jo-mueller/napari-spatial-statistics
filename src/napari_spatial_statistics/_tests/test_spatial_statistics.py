def test_spatial_stats_nhe(make_napari_viewer):

    from napari_spatial_statistics._neighborhood import knearest_ckdtree
    from napari_spatial_statistics._sample_data import make_random_points
    from napari_spatial_statistics._spatial_statistics import neighborhood_enrichment_test

    viewer = make_napari_viewer()
    # import napari
    # viewer = napari.Viewer()

    pts = make_random_points(spatial_size=100, n_classes=2)
    viewer.add_points(pts[0], **pts[1])

    pts1 = knearest_ckdtree(viewer.layers[0], n_neighbors=5)
    neighborhood_enrichment_test(viewer, pts1)

def test_spatial_stats_nhe2(make_napari_viewer):

    from napari_spatial_statistics._neighborhood import distance_ckdtree
    from napari_spatial_statistics._sample_data import make_random_points
    from napari_spatial_statistics._spatial_statistics import neighborhood_enrichment_test

    viewer = make_napari_viewer()
    # import napari
    # viewer = napari.Viewer()

    pts = make_random_points(spatial_size=100, n_classes=2)
    viewer.add_points(pts[0], **pts[1])

    pts1 = distance_ckdtree(viewer.layers[0], radius=10)
    neighborhood_enrichment_test(viewer, pts1)

if __name__ == "__main__":
    test_spatial_stats_nhe()
    test_spatial_stats_nhe2()
