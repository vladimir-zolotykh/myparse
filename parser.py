#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from __future__ import annotations
from typing import Iterator
from dataclasses import dataclass
from iter_tokens import Token, Tokens


# >>> e = ExpressionEvaluator()
# >>> e.parse('2')
# 2
# >>> e.parse('2 + 3')
# 5
# >>> e.parse('2 + 3 * 4')
# 14
# >>> e.parse('2 + (3 + 4) * 5')
# 37
# >>> e.parse('2 + (3 + * 4)')
# Traceback (most recent call last):
# ...
# SyntaxError: Expected NUMBER or LPAREN


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


class Parser:
    def __init__(self):
        self.tokens: Iterator[Token] | None = None  # type(None)
        # self.cash: TokensCash = None
        self.tok: Token | None = None

    def parse(self, str_to_parse: str):
        self.tokens = Tokens().iter_tokens(str_to_parse)
        # self.cash = TokensCash(str_to_parse)
        self._advance()
        return self.expr()

    def _advance(self) -> Token | None:
        try:
            self.tok = next(self.tokens)
            # self.tok = self.cash.next()
            return self.tok
        except StopIteration:
            return None

    def _expect(self, expected: str):
        if self.tok.val != expected:
            raise SyntaxError(f"{self.tok.val}: Expected {expected}")
        self._consume()

    def _consume(self) -> None:
        self.tok = next(self.tokens)
        # self.tok = self.cash.next()

    def expr(self) -> Node:
        res = self.term()
        while (op := self.tok) and op in ("+", "-"):
            self._consume()
            right = self.term()
            res = Plus("+", res, right) if op == "+" else Minus("-", res, right)
        return res

    def term(self) -> Node:
        res = self.factor()
        while (op := self.tok) and op in ("*", "/"):
            self._consume()
            right = self.factor()
            res = Mul("*", res, right) if op == "*" else Div("/", res, right)
        return res

    def factor(self) -> Node:
        tok = self.tok
        if tok == "(":
            self._consume()
            res = self.expr()
            self._expect(")")
        else:
            try:
                res = Num(float(tok.val))
                self._advance()
            except ValueError as exc:
                raise SyntaxError(f"{tok.val!r} Expected ( or NUMBER") from exc

        return res


if __name__ == "__main__":
    p = Parser()
    e = "2"
    res: Node = p.parse(e)
    print(f"{e = }, {res = }")
    e = "2 + 3"
    res = p.parse(e)
    print(f"{e = }, {res = }")
    e = "2 + 3 * 4"
    res = p.parse(e)
    print(f"{e = }, {res = }")
    e = "2 + (3 + 4) * 5"
    res = p.parse(e)
    print(f"{e = }, {res = }")
    e = "2 + (3 + * 4)"
    try:
        res = p.parse(e)
    except SyntaxError as exc:
        print(exc)
