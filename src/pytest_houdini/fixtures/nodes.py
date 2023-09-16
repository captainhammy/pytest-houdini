"""Fixtures related to nodes."""

# Future
from __future__ import annotations

# Standard Library
from typing import TYPE_CHECKING

# Third Party
import pytest

# Houdini
import hou

if TYPE_CHECKING:
    from collections.abc import Generator

# Non-Public Functions


def _find_matching_node(parent: hou.Node, request: pytest.FixtureRequest) -> hou.Node:
    """Try to find a matching child node based on a test request.

    Node search order is as follows:
    - Node matching the exact test name
    - Node matching the class name + test name (minus 'test_' prefix for function name)
    - Node matching the class name / test name (minus 'test_' prefix for function name)
    - Node matching the class name

    The class name can be either the raw name or entirely lowercase.

    Args:
        parent: The parent node to search under.
        request: A fixture request with which to find a node.

    Returns:
        A child node matching the request, if any.

    Raises:
         RuntimeError: Will be raised if no matching node could be found.

    """
    test_name = request.node.name

    # First try to find a node with the exact test name.
    names = [test_name]

    if request.cls is not None:
        cls_name = request.cls.__name__

        test_name = test_name[5:]

        # Look for a node with the class name + test name (minus test_ from function name)
        names.append(f"{cls_name}_{test_name}")
        names.append(f"{cls_name.lower()}_{test_name}")

        # Also support the test node being under a parent node based on the class name.
        names.append(f"{cls_name}/{test_name}")
        names.append(f"{cls_name.lower()}/{test_name}")

        # Finally try to find a node with the class name.
        names.append(cls_name)
        names.append(cls_name.lower())

    for name in names:
        node = parent.node(name)

        if node is not None:
            return node

    raise RuntimeError(
        f"Could not find any matching test nodes: {', '.join([parent.path() + '/' + name for name in names])}"
    )


# Fixtures


@pytest.fixture
def obj_test_node(request: pytest.FixtureRequest) -> Generator[hou.Node, None, None]:
    """Fixture to provide a node in /obj matching the test."""
    parent = hou.node("/obj")

    return _find_matching_node(parent, request)


@pytest.fixture
def obj_test_geo(obj_test_node: hou.Node) -> Generator[hou.Geometry, None, None]:
    """Fixture to provide the display node geometry of a node in /obj matching the test."""
    if obj_test_node.childTypeCategory() != hou.sopNodeTypeCategory():
        raise RuntimeError(f"{obj_test_node.path()} does not contain SOP nodes")

    return obj_test_node.displayNode().geometry()


@pytest.fixture
def obj_test_geo_copy(obj_test_geo: hou.Node) -> Generator[hou.Geometry, None, None]:
    """Fixture to get a writable copy of the display node geometry of a node in /obj matching the test."""
    geo = hou.Geometry()

    geo.merge(obj_test_geo)

    return geo


@pytest.fixture
def out_test_node(request: pytest.FixtureRequest) -> Generator[hou.Node, None, None]:
    """Fixture to provide a node in /out matching the test."""
    parent = hou.node("/out")

    return _find_matching_node(parent, request)
