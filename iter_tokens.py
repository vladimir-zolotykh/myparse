#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Any
from dataclasses import dataclass
import re


@dataclass
class Token:
    name: str
    val: Any


class TokensMeta(type):
    def __new__(mcls, clsname, bases, clsdict):
        for key, val in clsdict.items():
            if key not in ("__module__", "__qualname__"):
                if isinstance(val, str):
                    rval = rf"(?P<{key}>{val})"
                    clsdict[key] = rval
        return super().__new__(mcls, clsname, bases, clsdict)


class Tokens(metaclass=TokensMeta):
    NAME = r"[A-Za-z](\w|\d)+"  # r"(?P<NAME>[A-Za-z](\w|\d)+)"
    NUM = r"\d+"  # r"(?P<NUM>\d+)"

    def iter_tokens(self, str_to_parse):
        masterpat = "|".join(
            (val for val in self.__class__.__dict__.values() if isinstance(val, str))
        )
        print(f"{masterpat = }")
        for m in re.finditer(masterpat, str_to_parse):
            token = Token(m.lastgroup, m.group(0))
            yield token
            # if token.name != "WS":


if __name__ == "__main__":
    tokens = Tokens()
    for tok in tokens.iter_tokens("2 + (3 + 4) * 5"):
        print(tok)
