# Neighborhood enrichment test in image layer

### Data generation
<img src="./imgs/nhe_spots/1_generate_data.png" width=45% height=45%> <img src="./docs/imgs/nhe_spots/1_generated_data_widget.PNG" width=45% height=45%>

The settings of the data generator refer to the following properties:
- `n_points`: Number of points to be created
- `n_classes`: Number of point classes: Each "class" could, for instance, refer to a different cell type in a real experiment.
- `spatial_size`: The points will be distributed in a `[SxSxS]`-sized space. `S` can be set using this input.
- `dim`: Select whether data should be 2D/3D/4D.

The result (in 2D and 3D) will look like this:

<img src="./imgs/nhe_spots/1_generated_data.png" width=45% height=45%>

### Peak detection
Napari-spatial statistics provides a basic maxima detection as provided by [scikit-image ](https://scikit-image.org/docs/stable/api/skimage.feature.html#skimage.feature.peak_local_max). To use it, select it from `Plugins > napari-spatial-statistics > detect maxima` and use it **on each of the generated image layers**. This will create three separate points layers with each layer containing point data from one image layer:

<img src="./imgs/nhe_spots/2_detected_spots.png" width=45% height=45%>

Since napari-spatial-statistics operates on data stored in single point layers, you need to merge the separate points layers into a single layer. To do this, use `Plugins > napari-spatial-statistics > merge points layers` and lick `Run`. This will collect all present points layers and merge them into a single layer: 

<img src="./imgs/nhe_spots/2_detected_spots.png" width=45% height=45%>

You can now proceed with the analysis as described in [this tutorial](./demo_nhe_points_layer.md). Running the test described there generates a neighborhood enrichment matrix that denotes the enrichment score between all types of object:

<img src="./imgs/nhe_spots/3_result_nhe_matrix.png" width=45% height=45%>