def tst_spatial_stats_nhe(make_napari_viewer):

    from napari_spatial_statistics._neighborhood import knearest_ckdtree
    from napari_spatial_statistics._sample_data import make_random_points
    from napari_spatial_statistics._spatial_statistics import neighborhood_enrichment_test

    viewer = make_napari_viewer()
    # import napari
    # viewer = napari.Viewer()

    pts = make_random_points(spatial_size=100, n_classes=2)
    pts = knearest_ckdtree(pts, n_neighbors=5)
    neighborhood_enrichment_test(viewer, pts)

def tst_spatial_stats_nhe2():

    from napari_spatial_statistics._neighborhood import distance_ckdtree
    from napari_spatial_statistics._sample_data import make_random_points
    from napari_spatial_statistics._spatial_statistics import neighborhood_enrichment_test
    from napari.layers import Points

    # viewer = make_napari_viewer()
    import napari
    viewer = napari.Viewer()

    pts = make_random_points(spatial_size=100, n_classes=2)
    pts = viewer.add_points(pts[0], **pts[1])
    distance_ckdtree(pts, radius=10, show_neighborhood=False)


    wdg = neighborhood_enrichment_test()

if __name__ == "__main__":
    tst_spatial_stats_nhe2()
