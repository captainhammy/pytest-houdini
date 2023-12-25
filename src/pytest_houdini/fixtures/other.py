"""Other fixtures for testing."""

# Future
from __future__ import annotations

# Standard Library
from typing import Any, Callable

# Third Party
import pytest

# Fixtures


@pytest.fixture
def remove_abstract_methods(monkeypatch: pytest.MonkeyPatch) -> Callable:
    """Fixture to temporarily remove abstract methods from a class for testing purposes.

    Consider the following class definition with an abstract method and a concrete method which
    we want to test. Rather than creating a subclass for testing any non-abstract methods we
    can use the fixture to remove them during the test so that the object can be instantiated.

    class Foo(metaclass=abc.ABCMeta):

        @abc.abstractmethod
        def bar(self):
            pass

        def get_foo(self):
            return "foo"

    def test_get_foo(remove_abstract_methods):
        remove_abstract_methods(Foo)

        f = Foo()
        assert f.get_foo() == "foo"
    """

    def _remove_abstract(cls: Any) -> None:
        monkeypatch.setattr(cls, "__abstractmethods__", set())

    return _remove_abstract
