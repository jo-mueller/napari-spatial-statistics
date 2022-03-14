def test_spatial_stats_nhe():

    import napari
    from napari_spatial_statistics._neighborhood import knearest_ckdtree,\
        distance_ckdtree
    from napari_spatial_statistics._sample_data import make_random_points
    from napari_spatial_statistics._spatial_statistics import neighborhood_enrichment_test

    viewer = napari.Viewer()

    pts = make_random_points()
    viewer.add_points(pts[0], **pts[1])

    distance_ckdtree(viewer.layers[0], radius=10)
    neighborhood_enrichment_test(viewer, viewer.layers[0])

    knearest_ckdtree(viewer.layers[0], n_neighbors=5)
    neighborhood_enrichment_test(viewer, viewer.layers[0])

if __name__ == "__main__":
    test_spatial_stats_nhe()
