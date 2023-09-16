"""Test the pytest_houdini.fixtures.shelf_tools module."""

# Standard Library
import importlib

# pytest-houdini
import pytest_houdini.fixtures.shelf_tools

importlib.reload(pytest_houdini.fixtures.shelf_tools)

pytest_plugins = ["pytester"]


# Tests


def test_exec_shelf_tool_script(pytester, shared_datadir):
    """Test the 'exec_shelf_tool_script' fixture."""
    shelf_test_file = shared_datadir / "test_shelf_files.shelf"

    pytester.makepyfile(
        f"""
import pytest

from pytest_houdini.tools import does_not_raise

import hou

@pytest.mark.parametrize(
    "tool_name, raiser",
    (
        ("_not_a_tool_", pytest.raises(RuntimeError)),
        ("pytest_houdini_test_tool", does_not_raise()),
    )
)
def test_exec_shelf_tool_script(exec_shelf_tool_script, tool_name, raiser):
    hou.shelves.loadFile("{shelf_test_file.as_posix()}")

    scriptargs = {{"result": False}}

    with raiser:
        exec_shelf_tool_script(tool_name, scriptargs)

        assert scriptargs["result"]
"""
    )
    result = pytester.runpytest()

    result.assert_outcomes(passed=2)
