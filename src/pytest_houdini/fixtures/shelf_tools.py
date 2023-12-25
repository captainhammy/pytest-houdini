"""Testing fixtures for shelf tools."""

# Future
from __future__ import annotations

# Standard Library
from typing import Callable

# Third Party
import pytest

# pytest-houdini
from pytest_houdini.fixtures.exceptions import MissingToolError

# Houdini
import hou

# Fixtures


@pytest.fixture
def exec_shelf_tool_script() -> Callable:
    """Fixture to execute a shelf tool."""

    def _exec(tool_name: str, kwargs: dict) -> None:
        """Execute tool code inside a file.

        Args:
            tool_name: The name of the tool to execute.
            kwargs: The global 'kwargs' dict for the tool execution.

        Raises:
            MissingToolError: If a tool of the name cannot be found.
        """
        tool = hou.shelves.tool(tool_name)

        if tool is None:
            raise MissingToolError(tool_name)

        exec(tool.script(), {"kwargs": kwargs})

    return _exec
