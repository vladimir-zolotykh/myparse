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

    def __eq__(self, other):
        if isinstance(other, str):
            return self.val == other
        return self.val == other.val


class TokensMeta(type):
    def __iter__(cls):
        # cls : Tokens
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
    WS = r"\s+"

    def iter_tokens(self, str_to_parse):
        # self.__class__ : iter_tokens.Tokens
        masterpat = "|".join((getattr(self, key) for key in self.__class__))
        for m in re.finditer(masterpat, str_to_parse):
            tok = Token(m.lastgroup, m.group(0))
            if tok.name != "WS":
                yield tok


if __name__ == "__main__":
    tokens = Tokens()
    for tok in tokens.iter_tokens("2 + (3 + 4) * 5"):
        print(tok)
