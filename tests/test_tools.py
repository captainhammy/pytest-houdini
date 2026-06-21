"""Test the pytest_houdini.tools module."""

# Future
from __future__ import annotations

# Standard Library
import importlib
from contextlib import nullcontext

# Third Party
import pytest

# pytest-houdini
import pytest_houdini.exceptions
import pytest_houdini.tools

# Houdini
import hou

importlib.reload(pytest_houdini.tools)
importlib.reload(pytest_houdini.exceptions)

# Tests


@pytest.mark.parametrize(
    "category_name, destroy, raiser, expected",
    [
        ("Object", False, nullcontext(), hou.nodeType("Object/subnet")),
        ("Driver", True, nullcontext(), hou.nodeType("Driver/subnet")),
        ("Lop", False, nullcontext(), hou.nodeType("Lop/subnet")),
        ("Shop", True, nullcontext(), hou.nodeType("Shop/material")),
        ("Vop", False, nullcontext(), hou.nodeType("Vop/subnet")),
        ("Cop2", True, nullcontext(), hou.nodeType("CopNet/img")),
        ("Cop", False, nullcontext(), hou.nodeType("CopNet/copnet")),
        ("Sop", True, nullcontext(), hou.nodeType("Object/geo")),
        ("Dop", False, nullcontext(), hou.nodeType("Object/dopnet")),
        ("Top", True, nullcontext(), hou.nodeType("Object/topnet")),
        ("Manager", False, pytest.raises(pytest_houdini.exceptions.UnsupportedCategoryError), None),
    ],
)
def test_context_container(
    category_name: str,
    destroy: bool,
    raiser: nullcontext[None] | pytest.RaisesExc[pytest_houdini.exceptions.UnsupportedCategoryError],
    expected: hou.nodeType | None,
) -> None:
    """Test pytest_houdini.tools.context_container()."""
    category = hou.nodeTypeCategories().get(category_name)

    if category is None:
        pytest.skip(f"Category {category_name} not available in {hou.applicationVersionString()}")

    with raiser, pytest_houdini.tools.context_container(category, destroy=destroy) as container:
        assert container.type() == expected

    if expected is not None:
        # If the container was expected to be deleted, trying to access it will result in
        # a hou.ObjectWasDeleted exception, so use that to confirm it was deleted.
        persistence_raiser = pytest.raises(hou.ObjectWasDeleted) if destroy else nullcontext()

        with persistence_raiser:
            assert container.path()
