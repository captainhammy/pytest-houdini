"""Test the pytest_houdini.fixtures.ui module."""

# Standard Library
import importlib

# pytest-houdini
import pytest_houdini.fixtures.ui

importlib.reload(pytest_houdini.fixtures.ui)

pytest_plugins = ["pytester"]


# Tests


def test_mock_hdefereval(pytester):
    """Test the 'mock_hdefereval' fixture."""

    pytester.makepyfile(
        """
import hou

def test_mock_hdefereval(mock_hdefereval):
    import hdefereval

    assert hdefereval == mock_hdefereval

"""
    )
    result = pytester.runpytest()

    result.assert_outcomes(passed=1)


def test_mock_hou_qt(pytester):
    """Test the 'mock_hou_qt' fixture."""

    pytester.makepyfile(
        """
import hou

def test_mock_hou_qt(mock_hou_qt):
    assert hou.qt == mock_hou_qt

"""
    )
    result = pytester.runpytest()

    result.assert_outcomes(passed=1)


def test_mock_hou_ui(pytester):
    """Test the 'mock_hou_ui' fixture."""

    pytester.makepyfile(
        """
import hou

def test_mock_hou_ui(mock_hou_ui):
    assert hou.ui == mock_hou_ui

"""
    )
    result = pytester.runpytest()

    result.assert_outcomes(passed=1)


def test_set_ui_available(pytester):
    """Test the 'set_ui_available' fixture."""

    pytester.makepyfile(
        """
import hou

def test_set_ui_available(set_ui_available):
    assert hou.isUIAvailable()

"""
    )
    result = pytester.runpytest()

    result.assert_outcomes(passed=1)
