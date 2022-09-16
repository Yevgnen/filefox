# Table of Contents <span class="tag" tag-name="TOC"><span class="smallcaps">TOC</span></span>

- [Introduction](#introduction)
- [Installation](#installation)
  - [From pip](#from-pip)
  - [From source](#from-source)
- [Usages](#usages)
  - [Reading/Writing functions](#readingwriting-functions)
  - [Example](#example)
- [Contribution](#contribution)
  - [Formatting Code](#formatting-code)

# Introduction

`filefox` is a simple helper toolbox for reading and writing files.

# Installation

## From pip

``` bash
pip install filefox
```

## From source

``` bash
pip install git+https://github.com/Yevgnen/filefox.git
```

# Usages

## Reading/Writing functions

| Function       | Description                                                 |
|----------------|-------------------------------------------------------------|
| `read_json`    | Reading Json file                                           |
| `write_json`   | Writing Json file                                           |
| `read_pickle`  | Reading Pickle file                                         |
| `write_pickle` | Writing Pickle file                                         |
| `read_toml`    | Reading Toml file                                           |
| `write_toml`   | Writing Toml file                                           |
| `read_toml`    | Reading text file                                           |
| `write_toml`   | Writing text file                                           |
| `read`         | Detect file extension, decompress when necessary, read file |
| `write`        | Detect file extension, compress when necessary, write file  |

These functions have the following convention of their signatures:

- For all readers, the first positional argument is always the filename.
- For all writers, the first positional argument is always the dump object and the second is filename.
- All functions accpet a keyword argument `file_kwargs` which is an optional `dict` will be unpacked and passed to file opening function, e.g. `open` . The other keyword arguments will be passed to internal load/dump functions.

``` python
reader(filename, ..., file_kwargs=None, ...)
writer(obj, filename, ..., file_kwargs=None, ...)
```

## Example

``` python
# -*- coding: utf-8 -*-

# See and run examples/example.py

import filefox

expected = {
    "name": "John",
    "age": 12,
}

assert expected == filefox.read_json("json_data.json")
assert expected == filefox.read_json("json_data.json.gz")
assert expected == filefox.read("json_data.json")
assert expected == filefox.read("json_data.json.gz")
```

# Contribution

## Formatting Code

To ensure the codebase complies with a style guide, please use [flake8](https://github.com/PyCQA/flake8), [black](https://github.com/psf/black) and [isort](https://github.com/PyCQA/isort) tools to format and check codebase for compliance with PEP8.
