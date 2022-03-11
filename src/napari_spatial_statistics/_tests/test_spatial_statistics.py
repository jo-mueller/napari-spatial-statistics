from napari_spatial_statistics import neighborhood_enrichment_test, make_random_points
import numpy as np

# make_napari_viewer is a pytest fixture that returns a napari viewer object
# capsys is a pytest fixture that captures stdout and stderr output streams
def test_nhe_test()):
    # make viewer and add an image layer using our fixture
    viewer = make_napari_viewer()
    pts = make_random_points(n_points=200, number_of_layers=2)
    for pt in pts:
        viewer.add_points(pt[0], **pt[1])

    # create our widget, passing in the viewer
    neighborhood_enrichment_test(viewer, viewer.layers[0],
                                 viewer.layers[1], max_radius=300, sampling_rate=5,
                                 n_permutations=1000)
