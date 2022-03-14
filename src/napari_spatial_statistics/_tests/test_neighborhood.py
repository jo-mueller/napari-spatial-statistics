import numpy as np

def test_neighborhood(make_napari_viewer):

    from napari_spatial_statistics._neighborhood import knearest_ckdtree,\
        distance_ckdtree
    from napari_spatial_statistics._sample_data import make_random_points
    viewer = make_napari_viewer()

    pts = make_random_points()
    viewer.add_points(pts[0], **pts[1])

    knearest_ckdtree(viewer.layers[0])
    distance_ckdtree(viewer.layers[0])

if __name__ == "__main__":
    test_neighborhood()
