# -*- coding: utf-8 -*-

from typing import Iterable, TextIO, Union


def load(f: TextIO) -> str:
    return f.read()


def dump(text: Union[str, Iterable[str]], f: TextIO) -> None:
    if isinstance(text, str):
        f.write(text)
    else:
        f.writelines(text)

    return None
