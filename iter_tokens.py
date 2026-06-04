#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Any, MutableMapping
from dataclasses import dataclass
from collections import OrderedDict
import re


@dataclass
class Token:
    name: str
    val: Any


class TokensMeta(type):
    def __iter__(cls):
        yield from cls._token_names

    def __new__(mcls, clsname, bases, clsdict):
        token_names = []

        for key, val in clsdict.items():
            if key not in ("__module__", "__qualname__"):
                # key: NAME, NUM, iter_tokens
                if isinstance(val, str):
                    rval = rf"(?P<{key}>{val})"
                    clsdict[key] = rval
                    token_names.append(key)
        clsdict["_token_names"] = token_names
        return super().__new__(mcls, clsname, bases, clsdict)

    @classmethod
    def __prepare__(
        metacls, name: str, bases: tuple[type, ...], /, **kwds: Any
    ) -> MutableMapping[str, object]:
        return OrderedDict()


class Tokens(metaclass=TokensMeta):
    NAME = r"[A-Za-z](\w|\d)+"  # r"(?P<NAME>[A-Za-z](\w|\d)+)"
    NUM = r"\d+"  # r"(?P<NUM>\d+)"
    PLUS = r"\+"
    MINUS = r"-"
    MUL = r"\*"
    DIV = r"/"
    LPAREN = r"\("
    RPAREN = r"\)"
    WS = r"\w+"

    def iter_tokens(self, str_to_parse):
        masterpat = "|".join((getattr(self, key) for key in self.__class__))
        for m in re.finditer(masterpat, str_to_parse):
            yield Token(m.lastgroup, m.group(0))


if __name__ == "__main__":
    tokens = Tokens()
    for tok in tokens.iter_tokens("2 + (3 + 4) * 5"):
        print(tok)
