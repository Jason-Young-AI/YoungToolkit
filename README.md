# YoungToolkit
A Toolkit for a series of Young projects, these modules are very practical, basic, simple and easy to use, so you can import this package wherever you need to use it.

## Usage

``` python
from yoolkit.some_module import *
```

See [Full Documentation](https://jason-young.me/YoungToolkit/) for more details.

#### Table of Contents

* [Full Documentation](https://jason-young.me/YoungToolkit/)
* [visualizing](#visualizing)

#### visualizing
This module is a encapsulation of the client side of [visdom](https://github.com/facebookresearch/visdom), note that the visdom server API adheres to the [Plotly](https://plot.ly) convention of data and layout objects.

##### Visualizing Server

If you have not host a server of the visdom for yourself, please follow the instructions below.
```bash
export VISDOM_USERNAME="Jason"
export VISDOM_PASSWORD="123456"
export VISDOM_COOKIE="Guest_Visdom_Cookie"

function start_visdom {
    VISDOM_USE_ENV_CREDENTIALS=1 visdom -port 6789 -enable_login -force_new_cookie;
}

export -f start_visdom

nohup bash -c start_visdom > visdom.log 2>&1 &
```
or you can download the [start](https://github.com/Jason-Young-AI/YoungToolkit/blob/main/scripts/startv.sh) and [stop](https://github.com/Jason-Young-AI/YoungToolkit/blob/main/scripts/stopv.sh) scripts for convenience.

###### Visualizing Client

1. Setup visualizing client for the server you host (assume your host ip is 127.0.0.1):
```python
from yoolkit.visualizing import setup_visualizer
visualizer = setup_visualizer(
    'Demo',
    server='127.0.0.1',
    port=6789,
    username="Jason",
    password="123456",
    logging_path="demo.log",
    offline=False,
    overwrite=True
)
```

2. Open connection:
```python
visualizer.open()
```

3. Draw! Your paintings can be found at http://127.0.0.1:6789.
```python
import numpy
heat = numpy.arange(25).reshape((5,5))
visualizer.visualize(
    'heatmap',
    'demo_heatmap_5_5',
    'Demo 5*5 matrix heatmap',
    X=heat,
    opts={
        'colormap': 'Viridis',
    }
)
```
In method `visualizer.visualize()`, No.1 argument `visualize_type` is one of a methods of visdom like `line`, `heatmap`, `mesh`, etc., No.2 and No.3 arugment is `visualize_name` and `visualize_title`, all other keyword arguments is determined by `visualize_type` (refer to [visdom](https://github.com/facebookresearch/visdom) for more detailed usage documentation).

4. Close connection:
```python
visualizer.close()
```
After you close the connection between client and server, the server will remove the paintings that you have drawn.
Don't worry about that, all the paintings are saved in the logging file `demo.log` which is defined in step 1.

5. Replay a logging file:
```python
visualizer.replay_log('some_other.log')
```

## Installation
Three different installation methods are shown bellow:

1. Install `YoungToolkit` or `youngtoolkit` from PyPI:
``` bash
pip install YoungToolkit
```
or
``` bash
pip install youngtoolkit
```

2. Install `YoungToolkit` from sources:
```bash
git clone https://github.com/Jason-Young-AI/YoungToolkit.git
cd YoungToolkit
python setup.py install
```

3. Develop `YoungToolkit` locally:
```bash
git clone https://github.com/Jason-Young-AI/YoungToolkit.git
cd YoungToolkit
python setup.py build develop
```

## Installation with NVIDIA related functions supports

### Support IO for PyTorch Tensors

Append `[nv-io]` to the package name `YoungToolkit` durning the installation, like:
``` bash
pip install YoungToolkit[nv-io]
```

### Support Tracking of the GPU memory (PyTorch)

Append `[nv-track]` to the package name `YoungToolkit` durning the installation.
``` bash
pip install YoungToolkit[nv-track]
```
**NOTE**: I refer to project([Oldpan/Pytorch-Memory-Utils](https://github.com/Oldpan/Pytorch-Memory-Utils)) to implement this part [yoolkit.tracker](https://github.com/Jason-Young-AI/YoungToolkit/blob/main/yoolkit/tracker.py) 

### Support all features

Append `[full]` to the package name `YoungToolkit` durning the installation.
``` bash
pip install YoungToolkit[full]
```

**NOTATION** : If you are using `zsh` as your shell environment, please escape the square brackets or quote the argument like `pip install 'YoungToolkit[xxx]'`. ([Here](https://stackoverflow.com/a/30539963/5996506) is a more detailed explanation)
