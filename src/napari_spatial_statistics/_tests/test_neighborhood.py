import napari

def test_neighborhood():

    from napari_spatial_statistics._neighborhood import knearest_ckdtree,\
        distance_ckdtree, distance_squidpy
    from napari_spatial_statistics._sample_data import make_random_points

    pts = make_random_points()

    props_knearest = knearest_ckdtree(pts, show_neighborhood=False)
    props_ckdtree = distance_ckdtree(pts, show_neighborhood=False)
    props_squidpy = distance_squidpy(pts, show_neighborhood = False)

    assert 'neighbors' in props_knearest.keys()
    assert 'neighbors' in props_ckdtree.keys()
    assert 'neighbors' in props_squidpy.keys()

if __name__ == "__main__":
    test_neighborhood()
