# -*- coding: utf-8 -*-

from __future__ import annotations

import collections
import json
import os
from collections.abc import Callable, Mapping
from typing import Any, Optional, Union


def _wrap_reader(reader: Callable) -> Callable:
    def _wrapper(filename, *args, file_kwargs=None, **kwargs):
        if file_kwargs is None:
            file_kwargs = {"mode": "r"}

        with open(filename, **file_kwargs) as f:
            return reader(f, *args, **kwargs)

    return _wrapper


def _wrap_writer(writer: Callable) -> Callable:
    def _wrapper(filename, obj, *args, file_kwargs=None, **kwargs):
        if file_kwargs is None:
            file_kwargs = {"mode": "w"}

        with open(filename, **file_kwargs) as f:
            writer(obj, f, *args, **kwargs)

    return _wrapper


read_json = _wrap_reader(json.load)
write_json = _wrap_writer(json.dump)


class _Handler(collections.namedtuple("_Handler", ["reader", "writer"])):
    pass


_HANDLERS = {
    ".json": _Handler(read_json, write_json),
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
    filename: Union[str, os.PathLike],
    obj: Any,
    *args: tuple,
    file_kwargs: Optional[Mapping] = None,
    **kwargs: Mapping
) -> None:
    ext = os.path.splitext(filename)[1]
    handler = _HANDLERS.get(ext)
    if not handler:
        raise NotImplementedError()

    handler.writer(filename, obj, *args, file_kwargs=file_kwargs, **kwargs)


__version__ = "0.1.0"
