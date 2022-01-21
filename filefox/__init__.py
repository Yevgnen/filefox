# -*- coding: utf-8 -*-

from __future__ import annotations

import collections
import json
import os
import pickle
from collections.abc import Callable, Mapping
from typing import Any, Optional, Union

import pytoml


def _wrap_reader(reader: Callable, default_mode: str = "r") -> Callable:
    def _wrapper(filename, *args, file_kwargs=None, **kwargs):
        if file_kwargs is None:
            file_kwargs = {"mode": default_mode}

        with open(filename, **file_kwargs) as f:
            return reader(f, *args, **kwargs)

    return _wrapper


def _wrap_writer(writer: Callable, default_mode: str = "w") -> Callable:
    def _wrapper(obj, filename, *args, file_kwargs=None, **kwargs):
        if file_kwargs is None:
            file_kwargs = {"mode": default_mode}

        with open(filename, **file_kwargs) as f:
            writer(obj, f, *args, **kwargs)

    return _wrapper


read_json = _wrap_reader(json.load)
write_json = _wrap_writer(json.dump)
read_pickle = _wrap_reader(pickle.load, default_mode="rb")
write_pickle = _wrap_writer(pickle.dump, default_mode="wb")
read_toml = _wrap_reader(pytoml.load)
write_toml = _wrap_writer(pytoml.dump)


class _Handler(collections.namedtuple("_Handler", ["reader", "writer"])):
    pass


_HANDLERS = {
    ".json": _Handler(read_json, write_json),
    ".pickle": _Handler(read_pickle, write_pickle),
    ".pkl": _Handler(read_pickle, write_pickle),
    ".toml": _Handler(read_toml, write_toml),
}


def read(
    filename: Union[str, os.PathLike],
    *args: tuple,
    file_kwargs: Optional[Mapping] = None,
    **kwargs: Mapping
) -> Any:
    ext = os.path.splitext(filename)[1]
    handler = _HANDLERS.get(ext)
    if not handler:
        raise NotImplementedError()

    return handler.reader(filename, *args, file_kwargs=file_kwargs, **kwargs)


def write(
    obj: Any,
    filename: Union[str, os.PathLike],
    *args: tuple,
    file_kwargs: Optional[Mapping] = None,
    **kwargs: Mapping
) -> None:
    ext = os.path.splitext(filename)[1]
    handler = _HANDLERS.get(ext)
    if not handler:
        raise NotImplementedError()

    handler.writer(obj, filename, *args, file_kwargs=file_kwargs, **kwargs)


__version__ = "0.3.0"
