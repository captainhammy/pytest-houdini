"""Test the pytest_houdini.fixtures.soho module."""

# Standard Library
import importlib

# pytest-houdini
import pytest_houdini.fixtures.soho

importlib.reload(pytest_houdini.fixtures.soho)

pytest_plugins = ["pytester"]


# Tests


def test_patch_soho(pytester):
    """Test the 'patch_soho' fixture."""
    pytester.makepyfile(
        """
import hou

def test_patch_soho(patch_soho):
    import IFDapi
    assert IFDapi == patch_soho.IFDapi

    import IFDhooks
    assert IFDhooks == patch_soho.IFDhooks

    import IFDsettings
    assert IFDsettings == patch_soho.IFDsettings

    import mantra
    assert mantra == patch_soho.mantra

    import soho
    assert soho == patch_soho.soho

"""
    )
    result = pytester.runpytest()

    result.assert_outcomes(passed=1)
