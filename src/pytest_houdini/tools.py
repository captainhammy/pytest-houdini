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


# Functions


@contextmanager
def context_container(category: hou.NodeTypeCategory, *, destroy: bool = True) -> Generator[hou.OpNode, None, None]:
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

    # Types which can map directly to default scene nodes.
    direct_mappings = {
        "Driver": hou.node("/out"),
        "Lop": hou.node("/stage"),
        "Object": hou.node("/obj"),
        "Shop": hou.node("/shop"),
        "Vop": hou.node("/mat"),
    }

    container = direct_mappings.get(category_name)

    # If there was a direct mapping then use it.
    if container is not None:
        container = container.createNode("subnet")

        yield container

    # Otherwise, check for specific contexts and create the requisite node
    # of a matching context.
    else:
        if category_name == "Cop2":
            container = hou.node("/img").createNode("img")

        elif category_name == "Cop":
            container = hou.node("/img").createNode("copnet")

        elif category_name == "Sop":
            container = hou.node("/obj").createNode("geo")

        elif category_name == "Dop":
            container = hou.node("/obj").createNode("dopnet")

        elif category_name == "Top":
            container = hou.node("/obj").createNode("topnet")

        # If a known context cannot be found, raise an error.
        else:
            raise UnsupportedCategoryError(category)

        yield container

    # Destroy the created container.
    if destroy:
        container.destroy()
