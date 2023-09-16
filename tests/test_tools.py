"""Test the pytest_houdini.tools module."""

# pytest-houdini
import pytest_houdini.tools

# Tests


def test_does_not_raise():
    """Test pytest_houdini.tools.does_not_raise()

    This test is pretty useless and mostly just here for test coverage.
    """
    with pytest_houdini.tools.does_not_raise():
        x = 1

    assert x == 1
