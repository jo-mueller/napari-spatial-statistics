import numpy as np
from napari_spatial_statistics import make_random_points
from napari_spatial_statistics._spatial_statistics import neighborhood_enrichment_test
from napari_spatial_statistics._neighborhood import knearest_ckdtree

def test_spatial_stats_nhe():

    n_classes = 2
    pts = make_random_points(spatial_size=100, n_classes=n_classes)

    # Test knearest scipy
    properties = knearest_ckdtree(pts, n_neighbors=5)
    result = neighborhood_enrichment_test(pts[0], properties=properties,
                                          on_feature='Cell type',
                                          n_permutations=100)

    assert result is not None
    assert 'zscore' in list(result.keys()) and 'count' in list(result.keys())
    assert np.array_equal(result['zscore'].shape, np.array([n_classes, n_classes]))

def test_density_map(make_napari_viewer):

    from napari_spatial_statistics._spatial_statistics import density_map
    viewer = make_napari_viewer()
    pts = make_random_points(spatial_size=100, n_classes=1)
    viewer.add_points(pts[0], **pts[1])

    density = density_map(pts[0])
    viewer.add_image(density)
    assert len(viewer.layers) == 2

def test_density_map2(make_napari_viewer):

    from napari_spatial_statistics import density_map, detect_maxima, brain_section

    viewer = make_napari_viewer()
    image = brain_section()
    viewer.add_image(image)

    pts = detect_maxima(image,
                        minimal_distance=2, threshold_value=30)
    pts_layer = viewer.add_points(pts)
    pts_layer.size = 2

    density = density_map(pts)
    viewer.add_image(density)

if __name__ == '__main__':
    import napari
    test_spatial_stats_nhe()
