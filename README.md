# YoungToolkit
A Toolkit for a series of Young projects, these modules are very practical, basic, simple and easy to use, so you can import this package wherever you need to use it.

## Usage

``` python
from yoolkit.some_module import *
```

See [Full Documentation](https://jason-young.me/YoungToolkit/) for more details.

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
