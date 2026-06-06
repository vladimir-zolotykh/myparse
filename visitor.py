#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from functools import singledispatchmethod
from parser import Parser
import node as N


class Visitor:
    def visit(self, node: N.Node):
        self.name = f"visit{type(node).__name__}"
        func = getattr(self, self.name, self.visit_generic)
        return func(node)

    def visit_generic(self, node: N.Node):
        raise TypeError(f"No method {self.name} in type {self.__class__.__name__}")


class CalcDispatch:
    @singledispatchmethod
    def visit(self, node):
        raise NotImplementedError(f"No visit method for {node.__class__.__name__}")

    @visit.register
    def _(self, n: N.Num):
        return n.val

    @visit.register
    def _(self, n: N.Plus):
        return self.visit(n.left) + self.visit(n.right)

    @visit.register
    def _(self, n: N.Mul):
        return self.visit(n.left) * self.visit(n.right)

    @visit.register
    def _(self, n: N.Div):
        return self.visit(n.left) / self.visit(n.right)


class Calc(Visitor):
    def visitNum(self, node: N.Num):
        return node.val

    def visitPlus(self, node: N.Plus):
        return self.visit(node.left) + self.visit(node.right)

    def visitMul(self, node: N.Mul):
        return self.visit(node.left) * self.visit(node.right)

    def visitDiv(self, node: N.Div):
        return self.visit(node.left) / self.visit(node.right)


class Infix(Visitor):
    pass


if __name__ == "__main__":
    # e = "2 + (3 + 4) * 5"
    # expected = eval(e)
    # node: N.Node = Parser().parse(e)
    # print(f"{expected = }, got: {Calc().visit(node)}")

    e = "2 + (3 + 4) * 5"
    expected = eval(e)
    node: N.Node = Parser().parse(e)
    print(f"{expected = }, got: {CalcDispatch().visit(node)}")
