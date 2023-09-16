"""This module contains supporting tooling for testing in Houdini."""

# Future
from __future__ import annotations

# Standard Library
from contextlib import contextmanager
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator


# Functions


@contextmanager
def does_not_raise() -> Generator[None, None, None]:
    """Dummy context manager for testing.

    You can use this to help parametrize tests which may or may not raise exceptions.

    Consider the below test for a function which divides two values. As it does not
    validate any of the values it will result in ZeroDivisionError if value2 is 0. We
    can use does_not_raise() in conjunction with pytest.raises(ZeroDivisionError) in order
    to test a bunch of values and handle any expected exceptions.

    def divider(value1, value2):
        return value1 / value2

    @pytest.mark.parametrize(
        "value, expected, tester",
        [
            (0, None, pytest.raises(ZeroDivisionError)),
            (3.0, 0.3333333333333333, does_not_raise()),
        ],
    )
    def test_divider(value, tester):

        with tester:
            result = divider(1, value)

            assert result == expected

    """
    yield
