"""Testing fixtures for shelf tools."""

# Future
from __future__ import annotations

# Standard Library
from typing import TYPE_CHECKING, Callable

# Third Party
import pytest

# Houdini
import hou

if TYPE_CHECKING:
    from collections.abc import Generator


# Fixtures


@pytest.fixture
def exec_shelf_tool_script() -> Generator[Callable, None, None]:
    """Fixture to execute a shelf tool."""

    def _exec(tool_name: str, kwargs: dict) -> None:
        """Execute tool code inside a file.

        :param tool_name: The name of the tool to execute.
        :param kwargs: The global 'kwargs' dict for the tool execution.
        :return:

        """
        tool = hou.shelves.tool(tool_name)

        if tool is None:
            raise RuntimeError(f"Could not find tool: {tool_name}")

        exec(tool.script(), {"kwargs": kwargs})  # pylint: disable=exec-used

    yield _exec
