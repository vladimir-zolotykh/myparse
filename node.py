#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from dataclasses import dataclass


@dataclass
class Node:
    val: float | str

    def __repr__(self):
        return f"{self.__class__.__name__}({self.val!r})"


@dataclass
class BinaryOp(Node):
    left: Node
    right: Node

    def __repr__(self):
        return f"{self.__class__.__name__}({self.left!r}, {self.right!r})"


class Plus(BinaryOp):
    pass


class Minus(BinaryOp):
    pass


class Mul(BinaryOp):
    pass


class Div(BinaryOp):
    pass


class Num(Node):
    pass
