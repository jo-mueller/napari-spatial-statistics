from napari_spatial_statistics import neighborhood_enrichment_test, make_random_points
import numpy as np

# make_napari_viewer is a pytest fixture that returns a napari viewer object
# capsys is a pytest fixture that captures stdout and stderr output streams
def test_example_q_widget(make_napari_viewer, capsys):
    # make viewer and add an image layer using our fixture
    viewer = make_napari_viewer()
    pts = make_random_points(n_points=200, number_of_layers=2)
    for pt in pts:
        viewer.add_points(pt[0], **pt[1])

    # create our widget, passing in the viewer
    neighborhood_enrichment_test(viewer, viewer.layers[0],
                                 viewer.layers[1], max_radius=300, sampling_rate=5,
                                 n_permutations=1000)


    assert len(viewer.layers) == 2

def neighborhood_enrichment(make_napari_viewer, capsys):
    viewer = make_napari_viewer()


    # this time, our widget will be a MagicFactory or FunctionGui instance
    my_widget = example_magic_widget()

    # if we "call" this object, it'll execute our function
    my_widget(viewer.layers[0])

    # read captured output and check that it's as we expected
    captured = capsys.readouterr()
    assert captured.out == f"you have selected {layer}\n"

if __name__ == "__main__":
    import napari
    viewer = napari.Viewer()
