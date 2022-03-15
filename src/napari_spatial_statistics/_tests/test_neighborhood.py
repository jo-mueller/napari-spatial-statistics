def test_neighborhood():

    from napari_spatial_statistics._neighborhood import knearest_ckdtree,\
        distance_ckdtree,\
        delaunay_scipy

    from napari_spatial_statistics._sample_data import make_random_points

    import napari
    viewer = napari.Viewer()

    pts = make_random_points()
    viewer.add_points(pts[0], **pts[1])

    knearest_ckdtree(viewer.layers[0])
    distance_ckdtree(viewer.layers[0])
    delaunay_scipy(viewer.layers[0])


if __name__ == "__main__":
    test_neighborhood()
