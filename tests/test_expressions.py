import pytest
from node import Num, Plus, Mul
from parser import Parser


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
def test_valid_expressions(expr, expected):
    assert Parser().parse(expr) == expected


def test_invalid_expression():
    with pytest.raises(SyntaxError, match=r"\*.*Expected \( or NUMBER"):
        Parser().parse("2 + (3 + * 4)")
