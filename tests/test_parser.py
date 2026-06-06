# test_parser.py

import pytest

from parser import (
    Parser,
    Num,
    Plus,
    Minus,
    Mul,
    Div,
)


@pytest.fixture
def parser():
    return Parser()


@pytest.mark.parametrize(
    ("expr", "expected"),
    [
        (
            "2",
            Num(2.0),
        ),
        (
            "2 + 3",
            Plus(
                "+",
                Num(2.0),
                Num(3.0),
            ),
        ),
        (
            "2 - 3",
            Minus(
                "-",
                Num(2.0),
                Num(3.0),
            ),
        ),
        (
            "2 * 3",
            Mul(
                "*",
                Num(2.0),
                Num(3.0),
            ),
        ),
        (
            "6 / 2",
            Div(
                "/",
                Num(6.0),
                Num(2.0),
            ),
        ),
        (
            "2 + 3 * 4",
            Plus(
                "+",
                Num(2.0),
                Mul(
                    "*",
                    Num(3.0),
                    Num(4.0),
                ),
            ),
        ),
        (
            "2 * 3 + 4",
            Plus(
                "+",
                Mul(
                    "*",
                    Num(2.0),
                    Num(3.0),
                ),
                Num(4.0),
            ),
        ),
        (
            "2 + (3 + 4) * 5",
            Plus(
                "+",
                Num(2.0),
                Mul(
                    "*",
                    Plus(
                        "+",
                        Num(3.0),
                        Num(4.0),
                    ),
                    Num(5.0),
                ),
            ),
        ),
    ],
)
def test_parse_valid_expressions(parser, expr, expected):
    assert parser.parse(expr) == expected


@pytest.mark.parametrize(
    "expr",
    [
        "2 + (3 + * 4)",
        "*",
        "+",
        "( )",
        "2 + )",
    ],
)
def test_parse_invalid_expressions(parser, expr):
    with pytest.raises(SyntaxError):
        parser.parse(expr)


def test_parse_error_message(parser):
    with pytest.raises(SyntaxError, match=r"Expected \( or NUMBER"):
        parser.parse("2 + (3 + * 4)")
