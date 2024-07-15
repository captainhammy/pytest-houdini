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
    "category_name, destroy, raiser, expected",
    [
        ("Object", False, None, hou.nodeType("Object/subnet")),
        ("Driver", True, None, hou.nodeType("Driver/subnet")),
        ("Lop", False, None, hou.nodeType("Lop/subnet")),
        ("Shop", True, None, hou.nodeType("Shop/material")),
        ("Vop", False, None, hou.nodeType("Vop/subnet")),
        ("Cop2", True, None, hou.nodeType("CopNet/img")),
        ("Cop", False, None, hou.nodeType("CopNet/copnet")),
        ("Sop", True, None, hou.nodeType("Object/geo")),
        ("Dop", False, None, hou.nodeType("Object/dopnet")),
        ("Top", True, None, hou.nodeType("Object/topnet")),
        ("Manager", False, pytest.raises(UnsupportedCategoryError), None),
    ],
)
def test_context_container(category_name, destroy, raiser, expected):
    """Test pytest_houdini.tools.context_container()."""
    category = hou.nodeTypeCategories().get(category_name)

    if category is None:
        pytest.skip(f"Category {category_name} not available in {hou.applicationVersionString()}")

    if raiser is None:
        raiser = nullcontext()

    with raiser, pytest_houdini.tools.context_container(category, destroy=destroy) as container:
        assert container.type() == expected

    if expected is not None:
        # If the container was expected to be deleted, trying to access it will result in
        # a hou.ObjectWasDeleted exception so use that to confirm it was deleted.
        persistence_raiser = pytest.raises(hou.ObjectWasDeleted) if destroy else nullcontext()

        with persistence_raiser:
            assert container.path()
