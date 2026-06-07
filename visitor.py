#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
# flake8: noqa: F811
from typing import NoReturn, Generic, TypeVar, cast
from collections.abc import Callable
from functools import singledispatchmethod
from multipledispatch import dispatch
from parser import Parser
import node as N

T = TypeVar("T")


class Visitor(Generic[T]):
    def visit(self, node: N.Node) -> T:
        self.name = f"visit{type(node).__name__}"
        func = cast(Callable[[N.Node], T], getattr(self, self.name, self.visit_generic))
        return func(node)

    def visit_generic(self, node: N.Node) -> NoReturn:
        raise TypeError(f"No method {self.name} in type {self.__class__.__name__}")


class CalcMulti:
    @dispatch(N.Node)
    def visit(self, n) -> float:
        return float(n.val)

    @dispatch(N.Plus)
    def visit(self, n) -> float:
        return self.visit(n.left) + self.visit(n.right)

    @dispatch(N.Minus)
    def visit(self, n) -> float:
        return self.visit(n.left) - self.visit(n.right)

    @dispatch(N.Mul)
    def visit(self, n) -> float:
        return self.visit(n.left) * self.visit(n.right)

    @dispatch(N.Div)
    def visit(self, n) -> float:
        return self.visit(n.left) / self.visit(n.right)


class CalcDispatch:
    @singledispatchmethod
    def visit(self, node: N.Node) -> float:
        raise NotImplementedError(f"No visit method for {node.__class__.__name__}")

    @visit.register
    def _(self, n: N.Num) -> float:
        return float(n.val)

    @visit.register
    def _(self, n: N.Plus) -> float:
        return self.visit(n.left) + self.visit(n.right)

    @visit.register
    def _(self, n: N.Mul) -> float:
        return self.visit(n.left) * self.visit(n.right)

    @visit.register
    def _(self, n: N.Div) -> float:
        return self.visit(n.left) / self.visit(n.right)


class Calc(Visitor[float]):
    def visitNum(self, node: N.Num) -> float:
        return float(node.val)

    def visitPlus(self, node: N.Plus) -> float:
        return self.visit(node.left) + self.visit(node.right)

    def visitMul(self, node: N.Mul) -> float:
        return self.visit(node.left) * self.visit(node.right)

    def visitDiv(self, node: N.Div) -> float:
        return self.visit(node.left) / self.visit(node.right)


class Infix(Visitor):
    pass


if __name__ == "__main__":
    # e = "2 + (3 + 4) * 5"
    # expected = eval(e)
    # node: N.Node = Parser().parse(e)
    # print(f"{expected = }, got: {Calc().visit(node)}")

    # e = "2 + (3 + 4) * 5"
    # expected = eval(e)
    # node: N.Node = Parser().parse(e)
    # print(f"{expected = }, got: {CalcDispatch().visit(node)}")

    e = "2 + (3 + 4) * 5"
    expected = eval(e)
    node: N.Node = Parser().parse(e)
    print(f"{expected = }, got: {CalcMulti().visit(node)}")
