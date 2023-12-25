"""Exceptions raised by pytest-houdini."""

# Future
from __future__ import annotations

# Standard Library
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import hou


# Exceptions


class MissingToolError(Exception):
    """Exception raised when a matching tool cannot be found.

    Args:
        tool_name: The missing tool name.
    """

    def __init__(self, tool_name: str) -> None:
        super().__init__(f"Could not find tool: {tool_name}")


class NoModuleTestFileError(Exception):
    """Exception raised when a module test file cannot be found.

    Args:
        test_file: The test file stem (no extension.)
        extensions: The extensions which were checked.
    """

    def __init__(self, test_file: str, extensions: tuple[str, ...]) -> None:
        msg = f"Could not find a valid test hip: {test_file}{{{','.join(extensions)}}}"

        super().__init__(msg)


class NoTestNodeError(Exception):
    """Exception raised when no test node could be found.

    Args:
        searched_paths: The test node paths which were searched.
    """

    def __init__(self, searched_paths: list[str]) -> None:
        super().__init__(f"Could not find any matching test nodes: {', '.join(searched_paths)}")


class TestNodeDoesNotContainSOPsError(Exception):
    """Exception raised when a test node does not contain SOP nodes.

    Args:
        node: The node which does not contain SOP nodes.
    """

    def __init__(self, node: hou.OpNode) -> None:
        super().__init__(f"{node.path()} does not contain SOP nodes.")
