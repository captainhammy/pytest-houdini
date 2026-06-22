"""Fixtures related to nodes."""

# Future
from __future__ import annotations

# Standard Library
import contextlib
from typing import TYPE_CHECKING, Protocol, cast

# Third Party
import pytest

# pytest-houdini
from pytest_houdini.fixtures.exceptions import (
    NoTestNodeError,
    TestNodeDoesNotContainSOPsError,
    UnsupportedCategoryError,
)

# Houdini
import hou

if TYPE_CHECKING:
    from collections.abc import Callable, Iterator


# Globals

# Known types that can be created with their parent/node type.
_CREATABLE_CATEGORY_MAPPINGS = {
    "Cop2": ("/img", "img"),
    "Cop": ("/img", "copnet"),
    "Sop": ("/obj", "geo"),
    "Dop": ("/obj", "dopnet"),
    "Top": ("/obj", "topnet"),
}

# Types that can map directly to default scene nodes.
_DIRECT_CATEGORY_MAPPINGS = {
    "Driver": hou.node("/out"),
    "Lop": hou.node("/stage"),
    "Object": hou.node("/obj"),
    "Shop": hou.node("/shop"),
    "Vop": hou.node("/mat"),
}

# Classes


class CallableToCreateTempNode(Protocol):
    """Protocol for a callable object that creates a temporary node."""

    def __call__(  # noqa: D102 # pragma: no cover
        self, parent: hou.OpNode, node_type_name: str, node_name: str | None = None, *, run_init_scripts: bool = True
    ) -> hou.OpNode: ...


# Non-Public Functions


def _context_container(category: hou.NodeTypeCategory) -> hou.OpNode:
    """Create an appropriate node to create a node of the provided category under.

    Args:
        category: The node type category of the node to create.

    Returns:
        An appropriate parent node to create a node of the desired type under.

    Raises:
        ValueError: Raised if the category does not correspond to a known type.
    """
    category_name = category.name()

    container = _DIRECT_CATEGORY_MAPPINGS.get(category_name)

    # If there was a direct mapping, then use it.
    if container is not None:
        return container.createNode("subnet")

    # Otherwise, check for specific contexts and create the requisite node
    # of a matching context.
    create_data = _CREATABLE_CATEGORY_MAPPINGS.get(category_name)

    if create_data is not None:
        return hou.node(create_data[0]).createNode(create_data[1])

    raise UnsupportedCategoryError(category)


def _find_matching_node(parent: hou.OpNode, request: pytest.FixtureRequest) -> hou.OpNode:
    """Try to find a matching child node based on a test request.

    Node search order is as follows:
    - Node matching the exact test name
    - Node matching the class name and test name (minus 'test_' prefix for function name)
    - Node matching the class name / test name (minus 'test_' prefix for function name)
    - Node matching the class name

    The class name can be either the raw name or entirely lowercase.

    Args:
        parent: The parent node to search under.
        request: A fixture request with which to find a node.

    Returns:
        A child node matching the request, if any.

    Raises:
         NoTestNodeError: Will be raised if no matching node could be found.
    """
    test_name = request.node.originalname

    # First, try to find a node with the exact test name.
    names = [test_name]

    if request.cls is not None:
        cls_name = request.cls.__name__

        test_name = test_name[5:]

        names.extend([
            # Look for a node with the class name + test name (minus test_ from function name)
            f"{cls_name}_{test_name}",
            f"{cls_name.lower()}_{test_name}",
            # Also support the test node being under a parent node based on the class name.
            f"{cls_name}/{test_name}",
            f"{cls_name.lower()}/{test_name}",
            # Finally, try to find a node with the class name.
            cls_name,
            cls_name.lower(),
        ])

    for name in names:
        node = parent.node(name)

        if node is not None:
            return node

    searched_paths = [parent.path() + "/" + name for name in names]

    raise NoTestNodeError(searched_paths)


# Fixtures


@pytest.fixture
def create_temp_node() -> Iterator[CallableToCreateTempNode]:
    """Fixture to create a temporary node that will be destroyed on cleanup."""
    created_nodes_: list[hou.OpNode] = []

    def _create(
        parent: hou.OpNode, node_type_name: str, node_name: str | None = None, *, run_init_scripts: bool = True
    ) -> hou.OpNode:
        """Function to create a test node that will be destroyed on cleanup.

        Args:
            parent: The parent to create the test node under.
            node_type_name: The node type to create.
            node_name: Optional node name.
            run_init_scripts: Whether to run the node initialization scripts.

        Return:
            The created test node.
        """
        node = parent.createNode(node_type_name, node_name, run_init_scripts=run_init_scripts)

        created_nodes_.append(node)

        return node

    yield _create

    for created in created_nodes_:
        with contextlib.suppress(hou.ObjectWasDeleted):
            created.destroy()


@pytest.fixture
def create_context_container() -> Iterator[Callable[[hou.NodeTypeCategory], hou.OpNode]]:
    """Fixture to create an appropriate node to create a node under."""
    created_nodes_: list[hou.OpNode] = []

    def _create(category: hou.NodeTypeCategory) -> hou.OpNode:
        """Create a node suitable to create nodes of the supplied type category under.

        Args:
            category: The node type category of the node to create.

        Returns:
            An appropriate parent node to create a node of the desired type under.
        """
        container = _context_container(category)
        created_nodes_.append(container)

        return container

    yield _create

    for created in created_nodes_:
        with contextlib.suppress(hou.ObjectWasDeleted):
            created.destroy()


@pytest.fixture
def lop_test_node(request: pytest.FixtureRequest) -> hou.LopNode:
    """Fixture to provide a node in /stage matching the test."""
    parent = hou.node("/stage")

    return cast("hou.LopNode", _find_matching_node(parent, request))


@pytest.fixture
def obj_test_node(request: pytest.FixtureRequest) -> hou.ObjNode:
    """Fixture to provide a node in /obj matching the test."""
    parent = hou.node("/obj")

    return cast("hou.ObjNode", _find_matching_node(parent, request))


@pytest.fixture
def obj_test_geo(obj_test_node: hou.ObjNode) -> hou.Geometry:
    """Fixture to provide the read-only display node geometry of a node in /obj matching the test."""
    if obj_test_node.childTypeCategory() != hou.sopNodeTypeCategory():
        raise TestNodeDoesNotContainSOPsError(obj_test_node)

    return obj_test_node.displayNode().geometry()


@pytest.fixture
def obj_test_geo_copy(obj_test_geo: hou.Geometry) -> hou.Geometry:
    """Fixture to get a writable copy of the display node geometry of a node in /obj matching the test."""
    geo = hou.Geometry()

    geo.merge(obj_test_geo)

    return geo


@pytest.fixture
def out_test_node(request: pytest.FixtureRequest) -> hou.RopNode:
    """Fixture to provide a node in /out matching the test."""
    parent = hou.node("/out")

    return cast("hou.RopNode", _find_matching_node(parent, request))
