"""Test the pytest_houdini.fixtures.other module."""

# Standard Library
import importlib

# pytest-houdini
import pytest_houdini.fixtures.other

importlib.reload(pytest_houdini.fixtures.other)

pytest_plugins = ["pytester"]


# Tests


def test_remove_abstract_methods(pytester, shared_datadir):
    """Test the 'remove_abstract_methods' fixture."""

    pytester.makepyfile(
        """
import abc

def test_remove_abstract_methods(remove_abstract_methods):

    class TestClass(metaclass=abc.ABCMeta):
        def foo(self):
            print("foo")

        @abc.abstractmethod
        def bar(self):
            pass

    remove_abstract_methods(TestClass)

    f = TestClass()
    f.foo()

"""
    )
    result = pytester.runpytest()

    result.assert_outcomes(passed=1)
