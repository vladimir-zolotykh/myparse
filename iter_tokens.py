#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Any
import re
from collections import UserDict


class Token:
    name: str
    val: Any


class TokensMeta(type):
    def __new__(mcls, clsname, bases, clsdict):
        for key, val in clsdict.items():
            if isinstance(val, str):
                rval = rf"(?P<{key}>{val}"
                clsdict[key] = rval
                # self.data[key] = rval
        return super().__new__(mcls, clsname, bases, clsdict)


class Tokens(UserDict, metaclass=TokensMeta):
    NAME = r"[A-Za-z](\w|\d)+"  # r"(?P<NAME>[A-Za-z](\w|\d)+)"
    NUM = r"\d+"  # r"(?P<NUM>\d+)"

    def iter_tokens(self, str_to_parse):
        masterpat = "|".join((val for val in self.data.values()))
        for m in re.finditer(masterpat, str_to_parse):
            token = Token(m.lastgroup, m.group(1))
            if token.name != "WS":
                return token


if __name__ == "__main__":
    tokens = Tokens()
    tokens.iter_tokens("2 + (3 + 4) * 5")
