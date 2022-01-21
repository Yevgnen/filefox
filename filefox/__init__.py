# -*- coding: utf-8 -*-

from __future__ import annotations

import json
import os
from collections.abc import Mapping
from typing import Any, Optional, Union


def read(
    filename: Union[str, os.PathLike],
    *args: tuple,
    file_kwargs: Optional[Mapping] = None,
    **kwargs: Mapping
) -> Any:
    if not file_kwargs:
        file_kwargs = {"mode": "r"}

    ext = os.path.splitext(filename)[1]
    if ext == ".json":
        with open(filename, **file_kwargs) as f:
            return json.load(f, *args, **kwargs)

    raise NotImplementedError()


def write(
    filename: Union[str, os.PathLike],
    obj: Any,
    *args: tuple,
    file_kwargs: Optional[Mapping] = None,
    **kwargs: Mapping
) -> Any:
    if not file_kwargs:
        file_kwargs = {"mode": "w"}

    ext = os.path.splitext(filename)[1]
    if ext == ".json":
        with open(filename, **file_kwargs) as f:
            return json.dump(obj, f, *args, **kwargs)

    raise NotImplementedError()


__version__ = "0.1.0"
