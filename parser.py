#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from __future__ import annotations
from typing import Iterator, TypeVar
from iter_tokens import Token, Tokens
import node as N

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


T = TypeVar("T")


def require(val: T | None) -> T:
    assert val is not None, "Cannot happen"
    return val


class Parser:
    def __init__(self):
        self.tokens: Iterator[Token] | None = None  # type(None)
        self.tok: Token | None = None

    def parse(self, str_to_parse: str) -> N.Node:
        self.tokens = Tokens().iter_tokens(str_to_parse)
        self._advance()
        return self.expr()

    def _advance(self) -> Token | None:
        try:
            self.tok = next(require(self.tokens))
            return self.tok
        except StopIteration:
            return None

    def _expect(self, expected: str) -> None:
        self.tok = require(self.tok)
        if self.tok.val != expected:
            raise SyntaxError(f"{self.tok.val}: Expected {expected}")
        self._consume()

    def _consume(self) -> None:
        self.tok = next(require(self.tokens))

    def expr(self) -> N.Node:
        res = self.term()
        while (op := self.tok) and op in ("+", "-"):
            self._consume()
            right = self.term()
            res = N.Plus("+", res, right) if op == "+" else N.Minus("-", res, right)
        return res

    def term(self) -> N.Node:
        res = self.factor()
        while (op := self.tok) and op in ("*", "/"):
            self._consume()
            right = self.factor()
            res = N.Mul("*", res, right) if op == "*" else N.Div("/", res, right)
        return res

    def factor(self) -> N.Node:
        tok = require(self.tok)
        if tok == "(":
            self._consume()
            res = self.expr()
            self._expect(")")
        else:
            try:
                res = N.Num(float(tok.val))
                self._advance()
            except ValueError as exc:
                raise SyntaxError(f"{tok.val!r} Expected ( or NUMBER") from exc

        return res


if __name__ == "__main__":
    p = Parser()
    e = "2"
    res: N.Node = p.parse(e)
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
