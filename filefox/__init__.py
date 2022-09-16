# -*- coding: utf-8 -*-

from __future__ import annotations

import bz2
import collections
import gzip
import json
import lzma
import os
import pickle
from collections.abc import Callable, Mapping
from typing import Any, Optional, Union

import pytoml

from filefox import text


class BaseError(Exception):
    pass


class UnsupportedCompressionMethod(BaseError):
    def __init__(self, *args, ext=None):
        super().__init__(*args)
        self.ext = ext


class UnsupportedFileType(BaseError):
    def __init__(self, *args, ext=None):
        super().__init__(*args)
        self.ext = ext


class UnknownFileType(BaseError):
    def __init__(self, *args, filename=None):
        super().__init__(*args)
        self.filename = filename


_COMPRESSION = {
    ".bz2": bz2.open,
    ".gz": gzip.open,
    ".xz": lzma.open,
}


def _get_open_fn(filename):
    ext = os.path.splitext(filename)[1]
    open_fn = _COMPRESSION.get(ext, open)

    return open_fn


def _wrap_reader(reader: Callable, default_mode: str = "rt") -> Callable:
    def _wrapper(filename, *args, file_kwargs=None, **kwargs):
        if file_kwargs is None:
            file_kwargs = {"mode": default_mode}

        with _get_open_fn(filename)(filename, **file_kwargs) as f:
            return reader(f, *args, **kwargs)

    return _wrapper


def _wrap_writer(writer: Callable, default_mode: str = "wt") -> Callable:
    def _wrapper(obj, filename, *args, file_kwargs=None, **kwargs):
        if file_kwargs is None:
            file_kwargs = {"mode": default_mode}

        with _get_open_fn(filename)(filename, **file_kwargs) as f:
            writer(obj, f, *args, **kwargs)

    return _wrapper


read_json = _wrap_reader(json.load)
write_json = _wrap_writer(json.dump)
read_pickle = _wrap_reader(pickle.load, default_mode="rb")
write_pickle = _wrap_writer(pickle.dump, default_mode="wb")
read_toml = _wrap_reader(pytoml.load)
write_toml = _wrap_writer(pytoml.dump)
read_text = _wrap_reader(text.load)
write_text = _wrap_writer(text.dump)


class _Handler(collections.namedtuple("_Handler", ["reader", "writer"])):
    pass


_FILE_HANDLERS = {
    ".json": _Handler(read_json, write_json),
    ".pickle": _Handler(read_pickle, write_pickle),
    ".pkl": _Handler(read_pickle, write_pickle),
    ".toml": _Handler(read_toml, write_toml),
    ".txt": _Handler(read_text, write_text),
}


def _get_handler(filename):
    basename, compression_ext = os.path.splitext(filename)
    if not compression_ext:
        raise UnknownFileType("Failed to detect file type", filename=filename)

    basename, file_ext = os.path.splitext(basename)
    if not file_ext and compression_ext not in _COMPRESSION:
        file_ext = compression_ext
        compression_ext = ""

    if compression_ext and compression_ext not in _COMPRESSION:
        raise UnsupportedCompressionMethod(
            f"Unsupported compression method: {compression_ext}", ext=compression_ext
        )

    handler = _FILE_HANDLERS.get(file_ext)
    if not handler:
        raise UnsupportedFileType(f"Unsupported file type: {file_ext}", ext=file_ext)

    return handler


def read(
    filename: Union[str, os.PathLike],
    *args: tuple,
    file_kwargs: Optional[Mapping] = None,
    **kwargs: Mapping,
) -> Any:
    handler = _get_handler(filename)

    return handler.reader(filename, *args, file_kwargs=file_kwargs, **kwargs)


def write(
    obj: Any,
    filename: Union[str, os.PathLike],
    *args: tuple,
    file_kwargs: Optional[Mapping] = None,
    **kwargs: Mapping,
) -> None:
    handler = _get_handler(filename)

    handler.writer(obj, filename, *args, file_kwargs=file_kwargs, **kwargs)


__all__ = [
    "read",
    "write",
    "read_json",
    "write_json",
    "read_pickle",
    "write_pickle",
    "read_toml",
    "write_toml",
    "BaseError",
    "UnsupportedCompressionMethod",
    "UnsupportedFileType",
    "UnknownFileType",
]
__version__ = "0.5.0"
