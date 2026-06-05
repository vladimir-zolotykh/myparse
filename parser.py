#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from __future__ import annotations
from typing import Iterator, Any
from dataclasses import dataclass
import logging
from functools import wraps
import copy
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


def log_tokens(func):
    @wraps(func)
    def wrapper(*args, **kwds):
        self = args[0]
        # cash0 = copy.copy(self.cash)
        res = func(*args, **kwds)
        logging.info(f"[{func.__name__}] {self.cash!r}")
        return res

    return wrapper


class TokensCash:
    def __init__(self, str_to_parse: str):
        self._tokens = Tokens().iter_tokens(str_to_parse)
        self._cash: list[Token] = list(self._tokens)
        logging.info(f"[TokensCash.__init__] {self._cash!r}")
        self._index = 0

    def next(self) -> Token:
        try:
            val: Token = self._cash[self._index]
            self._index += 1
            return val
        except IndexError:
            raise StopIteration

    def __repr__(self):
        return ", ".join(repr(tok) for tok in self._cash[: self._index])


class Parser:
    def __init__(self):
        # self.tokens: Iterator[Token] | None = None  # type(None)
        self.cash: TokensCash = None
        self.tok: Token | None = None

    def parse(self, str_to_parse: str):
        logging.info(f"[parse] {str_to_parse = }")

        # self.tokens = Tokens().iter_tokens(str_to_parse)
        self.cash = TokensCash(str_to_parse)
        self._advance()
        return self.expr()

    @log_tokens
    def _advance(self) -> Token | None:
        try:
            # self.tok = next(self.tokens)
            self.tok = self.cash.next()
            return self.tok
        except StopIteration:
            return None

    @log_tokens
    def _expect(self, expected: str):
        if self.tok.val != expected:
            raise SyntaxError(f"{self.tok.val}: Expected {expected}")
        self._consume()

    @log_tokens
    def _consume(self) -> None:
        # self.tok = next(self.tokens)
        self.tok = self.cash.next()

    @log_tokens
    def expr(self) -> Node:
        res = self.term()
        # while (op := self._advance()) and op.val in ("+", "-"):
        while (op := self.tok) and op.val in ("+", "-"):
            self._consume()
            right = self.term()
            res = Plus("+", res, right) if op.val == "+" else Minus("-", res, right)
        return res

    @log_tokens
    def term(self) -> Node:
        res = self.factor()
        # while (op := self._advance()) and op.val in ("*", "/"):
        while (op := self.tok) and op.val in ("*", "/"):
            self._consume()
            right = self.factor()
            res = Mul("*", res, right) if op.val == "*" else Div("/", res, right)
        return res

    @log_tokens
    def factor(self) -> Node:
        # tok: Token = self._advance()
        tok = self.tok
        if tok.val == "(":
            self._consume()
            res = self.expr()
            self._expect("(")
        else:
            res = Num(tok.val)
            self._advance()
        return res


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    p = Parser()
    # res: Node = p.parse("2")
    res = p.parse("2 + 3")
    print(res)
    # res = p.parse("2 + 3 * 4")
    # res = p.parse("2 + (3 + 4) * 5")
    # res = p.parse("2 + (3 + * 4)")
