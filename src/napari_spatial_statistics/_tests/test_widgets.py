def test_nhetest_widget(make_napari_viewer):
    from napari_spatial_statistics._spatial_statistics import nhe_test_widget

    viewer = make_napari_viewer()
    n_wdgts = len(viewer.window._dock_widgets)
    wdg = nhe_test_widget(viewer)
    viewer.window.add_dock_widget(wdg)

    assert len(viewer.window._dock_widgets) == n_wdgts + 1

def test_plot_widget(make_napari_viewer):
    from napari_spatial_statistics._plot_widget import PlotWidget

    viewer = make_napari_viewer()
    n_wdgts = len(viewer.window._dock_widgets)
    wdg = PlotWidget(viewer)
    viewer.window.add_dock_widget(wdg)

    assert len(viewer.window._dock_widgets) == n_wdgts + 1

if __name__ == "__main__":

    import napari
    test_nhetest_widget(napari.Viewer)
