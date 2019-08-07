# jinete

[![PyPI](https://img.shields.io/pypi/v/jinete.svg)](https://pypi.org/project/jinete)
[![Read the Docs](https://img.shields.io/readthedocs/jinete.svg)](https://jinete.readthedocs.io/)
[![Travis (.org) branch](https://img.shields.io/travis/garciparedes/jinete/master.svg)](https://travis-ci.org/garciparedes/jinete/branches)
[![Coveralls github](https://img.shields.io/coveralls/github/garciparedes/jinete.svg)](https://coveralls.io/github/garciparedes/jinete)
[![GitHub](https://img.shields.io/github/license/garciparedes/jinete.svg)](https://github.com/garciparedes/jinete/blob/master/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/garciparedes/jinete.svg)](https://github.com/garciparedes/jinete)

## Description 

High Performance solving suite for the Pickup and Delivery Problem and its related extensions. 

*IMPORTANT*: This project is still under its early stage of development. So it's not recommended yet to use on real world projects. 

This library has been inspired (and created) by development from a Final Degree Project, which you can read at: https://github.com/garciparedes/tfg-pickup-and-delivery


## How to install

```bash
pip install jinete
```

## Getting Started

```python
import jinete as jit

dispatcher = jit.StaticDispatcher(
    partial(jit.FileLoader, file_path=file_path),
    jit.GreedyAlgorithm,
    partial(jit.PromptStorer, formatter_cls=jit.ColumnarStorerFormatter),
)

dispatcher.run()
```

## Documentation
You can find the documentation at: https://jinete.readthedocs.io/


## Development

You can install it simply typing:

```bash
pipenv install --dev
```

To run the tests perform:

```bash
pipenv python -m unittest discover tests
```

## Repository Contents

* [`examples`](examples/): Basic examples to start using the library.
* [`jinete`](jinete/): The source code of the library.
* [`tests`](tests/): The library tests.

## LICENSE
This project is licensed under [MIT](LICENSE) license.
