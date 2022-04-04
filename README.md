# napari-spatial-statistics

[![License](https://img.shields.io/pypi/l/napari-spatial-statistics.svg?color=green)](https://github.com/jo-mueller/napari-spatial-statistics/raw/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/napari-spatial-statistics.svg?color=green)](https://pypi.org/project/napari-spatial-statistics)
[![Python Version](https://img.shields.io/pypi/pyversions/napari-spatial-statistics.svg?color=green)](https://python.org)
[![tests](https://github.com/jo-mueller/napari-spatial-statistics/workflows/tests/badge.svg)](https://github.com/jo-mueller/napari-spatial-statistics/actions)
[![codecov](https://codecov.io/gh/jo-mueller/napari-spatial-statistics/branch/main/graph/badge.svg)](https://codecov.io/gh/jo-mueller/napari-spatial-statistics)
[![napari hub](https://img.shields.io/endpoint?url=https://api.napari-hub.org/shields/napari-spatial-statistics)](https://napari-hub.org/plugins/napari-spatial-statistics)

Analyze architecture of spatially distributed objects.

This plugins aims to make methods for spatial statistics available in Napari. Common usecases for spatial statistics are described in [this paper](https://www.frontiersin.org/articles/10.3389/fphys.2022.832417/full). In brief, methods of spatial statistics allow to answer questions like the following:
- Single type of objects in space: Do the objects appear clustered together or are they randomly scattered throughout space?
- Two or multiple types of objects: Does object of typa A appear within the neighborhood of tybe B objects more often than what we would expect from randomly distributed objects?

----------------------------------

## Usage

Napari-spatial-statistics currently allows analyzing spatial distributions of point and image layers in Napari. This tutorial describes a typical workflow for either image type and analysis:

| | Points layer data |  Image layer data  |
| ---| ---| --- |
|Neighborhood enrichment test | <img src="./docs/imgs/nhe_points/1_generate_data_2.png" width=45% height=45%> |



## Future features
- Cluster co-occurence statistics
- Ripley's functions
- Newman's assortativity
- Native integration with label layers

This [napari] plugin was generated with [Cookiecutter] using [@napari]'s [cookiecutter-napari-plugin] template.


## Installation

If you haven't already done so, create a new environment for Napari with:

```
conda create -n napari-spatial-statistics Python=3.9
conda activate napari-spatial-statistics
```

Install a few packages with conda:

```
conda install -c conda-forge napari h5py pytables
```

Finally, install `napari-spatial-statistics` via [pip]:

    pip install napari-spatial-statistics



To install latest development version :

    pip install git+https://github.com/jo-mueller/napari-spatial-statistics.git


## Contributing

Contributions are very welcome. Tests can be run with [tox], please ensure
the coverage at least stays the same before you submit a pull request.

## License

Distributed under the terms of the [BSD-3] license,
"napari-spatial-statistics" is free and open source software

## Issues

If you encounter any problems, please [file an issue] along with a detailed description.

[napari]: https://github.com/napari/napari
[Cookiecutter]: https://github.com/audreyr/cookiecutter
[@napari]: https://github.com/napari
[MIT]: http://opensource.org/licenses/MIT
[BSD-3]: http://opensource.org/licenses/BSD-3-Clause
[GNU GPL v3.0]: http://www.gnu.org/licenses/gpl-3.0.txt
[GNU LGPL v3.0]: http://www.gnu.org/licenses/lgpl-3.0.txt
[Apache Software License 2.0]: http://www.apache.org/licenses/LICENSE-2.0
[Mozilla Public License 2.0]: https://www.mozilla.org/media/MPL/2.0/index.txt
[cookiecutter-napari-plugin]: https://github.com/napari/cookiecutter-napari-plugin

[file an issue]: https://github.com/jo-mueller/napari-spatial-statistics/issues

[napari]: https://github.com/napari/napari
[tox]: https://tox.readthedocs.io/en/latest/
[pip]: https://pypi.org/project/pip/
[PyPI]: https://pypi.org/
