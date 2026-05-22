"""This module contains supporting tooling for testing in Houdini."""

# Future
from __future__ import annotations

# Standard Library
from contextlib import contextmanager
from typing import TYPE_CHECKING

# pytest-houdini
from pytest_houdini.exceptions import UnsupportedCategoryError

# Houdini
import hou

if TYPE_CHECKING:
    from collections.abc import Generator

# Globals

# Known types that can be created with their parent/node type.
_CREATABLE_CATEGORY_MAPPINGS = {
    "Cop2": ("/img", "img"),
    "Cop": ("/img", "copnet"),
    "Sop": ("/obj", "geo"),
    "Dop": ("/obj", "dopnet"),
    "Top": ("/obj", "topnet"),
}

# Types which can map directly to default scene nodes.
_DIRECT_CATEGORY_MAPPINGS = {
    "Driver": hou.node("/out"),
    "Lop": hou.node("/stage"),
    "Object": hou.node("/obj"),
    "Shop": hou.node("/shop"),
    "Vop": hou.node("/mat"),
}


# Functions


@contextmanager
def context_container(category: hou.NodeTypeCategory, *, destroy: bool = True) -> Generator[hou.OpNode]:
    """Context manager that provides an appropriate node to create a node under.

    >>> with context_container(hou.sopNodeTypeCategory()) as parent:
    ...     parent.createNode("box")

    Args:
        category: The node type category of the node to create.
        destroy: Whether to destroy the node after the scope ends.

    Returns:
        An appropriate parent node to create a node of the desired type under.

    Raises:
        ValueError: Raised if the category does not correspond to a known type.
    """
    category_name = category.name()

    container = _DIRECT_CATEGORY_MAPPINGS.get(category_name)

    # If there was a direct mapping then use it.
    if container is not None:
        container = container.createNode("subnet")

    # Otherwise, check for specific contexts and create the requisite node
    # of a matching context.
    else:
        create_data = _CREATABLE_CATEGORY_MAPPINGS.get(category_name)

        if create_data is not None:
            container = hou.node(create_data[0]).createNode(create_data[1])

        else:
            raise UnsupportedCategoryError(category)

    try:
        yield container

    finally:
        # Destroy the created container.
        if destroy:
            container.destroy()
