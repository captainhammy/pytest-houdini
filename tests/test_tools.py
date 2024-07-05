"""Test the pytest_houdini.tools module."""

# Standard Library
from contextlib import nullcontext

# Third Party
import pytest

# pytest-houdini
import pytest_houdini.tools
from pytest_houdini.exceptions import UnsupportedCategoryError

# Houdini
import hou

# Tests


@pytest.mark.parametrize(
    "category, raiser, expected",
    [
        (hou.objNodeTypeCategory(), nullcontext(), hou.node("/obj")),
        (hou.ropNodeTypeCategory(), nullcontext(), hou.node("/out")),
        (hou.lopNodeTypeCategory(), nullcontext(), hou.node("/stage")),
        (hou.shopNodeTypeCategory(), nullcontext(), hou.node("/shop")),
        (hou.cop2NodeTypeCategory(), nullcontext(), hou.nodeType("CopNet/img")),
        # (hou.copNodeTypeCategory(), nullcontext(), hou.nodeType("CopNet/copnet")),
        (hou.sopNodeTypeCategory(), nullcontext(), hou.nodeType("Object/geo")),
        (hou.dopNodeTypeCategory(), nullcontext(), hou.nodeType("Object/dopnet")),
        (hou.topNodeTypeCategory(), nullcontext(), hou.nodeType("Object/topnet")),
        (hou.managerNodeTypeCategory(), pytest.raises(UnsupportedCategoryError), None),
    ],
)
def test_context_container(category, raiser, expected):
    """Test pytest_houdini.tools.context_container()."""
    if category is None:
        return

    # Keep track if the container is expected to be deleted based on whether
    # the expected object is a node type (specific temporary container)
    expect_delete = isinstance(expected, hou.NodeType)

    with raiser, pytest_houdini.tools.context_container(category) as container:
        if isinstance(expected, hou.Node):
            assert container == expected

        else:
            assert container.type() == expected

    if expected is not None:
        # If the container was expected to be deleted, trying to access it will result in
        # a hou.ObjectWasDeleted exception so use that to confirm it was deleted.
        persistence_raiser = pytest.raises(hou.ObjectWasDeleted) if expect_delete else nullcontext()

        with persistence_raiser:
            container.path()
