#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from __future__ import annotations
from typing import Iterator, Any
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


@dataclass
class BinaryOp(Node):
    left: Node
    right: Node


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
        self.tok: Token | None = None

    def parse(self, str_to_parse: str):
        self.tokens = Tokens().iter_tokens(str_to_parse)
        self._advance()
        return self.expr()

    def _advance(self) -> Token | None:
        try:
            self.tok = next(self.tokens)
            return self.tok
        except StopIteration:
            return None

    def _expect(self, expected: str):
        if self.tok.val != expected:
            raise SyntaxError(f"{self.tok.val}: Expected {expected}")
        self._consume()

    def _consume(self) -> None:
        self.tok = next(self.tokens)

    def expr(self) -> Node:
        res = self.term()
        while (op := self._advance()) and op.val in ("+", "-"):
            right = self.term()
            res = Plus("+", res, right) if op == "+" else Minus("-", res, right)
        return res

    def term(self) -> Node:
        res = self.factor()
        while (op := self._advance()) and op in ("*", "/"):
            right = self.term()
            res = Mul("*", res, right) if op == "*" else Div("/", res, right)
        return res

    def factor(self) -> Node:
        tok: Token = self._advance()
        if tok.val == "(":
            self._consume()
            res = self.expr()
            self._expect("(")
        else:
            res = Num(tok)
            self._advance()
            return res


if __name__ == "__main__":
    p = Parser()
    res: Node = p.parse("2 + (3 + 4) * 5")
    print(res)
