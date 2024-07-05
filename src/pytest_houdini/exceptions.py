"""Exceptions raised by pytest-houdini."""

# Future
from __future__ import annotations

# Standard Library
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import hou


# Exceptions


class UnsupportedCategoryError(ValueError):
    """Exception raised when an invalid node type category is passed.

    Args:
        category: The invalid node type category.
    """

    def __init__(self, category: hou.NodeTypeCategory) -> None:
        super().__init__(f"Unknown category type {category.name()}")
