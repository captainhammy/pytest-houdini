"""Test the pytest_houdini.fixtures.nodes module."""

# Future
from __future__ import annotations

# Standard Library
import importlib
from contextlib import nullcontext
from typing import TYPE_CHECKING

# Third Party
import pytest

# pytest-houdini
import pytest_houdini.fixtures.nodes
from pytest_houdini.fixtures.exceptions import UnsupportedCategoryError

# Houdini
import hou

if TYPE_CHECKING:
    from pathlib import Path

importlib.reload(pytest_houdini.fixtures.nodes)

pytest_plugins = ["pytester"]


# Tests


@pytest.mark.parametrize(
    "category_name, raiser, expected",
    [
        ("Object", nullcontext(), hou.nodeType("Object/subnet")),
        ("Driver", nullcontext(), hou.nodeType("Driver/subnet")),
        ("Lop", nullcontext(), hou.nodeType("Lop/subnet")),
        ("Shop", nullcontext(), hou.nodeType("Shop/material")),
        ("Vop", nullcontext(), hou.nodeType("Vop/subnet")),
        ("Cop2", nullcontext(), hou.nodeType("CopNet/img")),
        ("Cop", nullcontext(), hou.nodeType("CopNet/copnet")),
        ("Sop", nullcontext(), hou.nodeType("Object/geo")),
        ("Dop", nullcontext(), hou.nodeType("Object/dopnet")),
        ("Top", nullcontext(), hou.nodeType("Object/topnet")),
        ("Manager", pytest.raises(UnsupportedCategoryError), None),
    ],
)
def test__context_container(
    category_name: str,
    raiser: nullcontext[None] | pytest.RaisesExc[UnsupportedCategoryError],
    expected: hou.nodeType | None,
) -> None:
    """Test pytest_houdini.fixtures.nodes._context_container()."""
    category = hou.nodeTypeCategories().get(category_name)

    if category is None:
        pytest.skip(f"Category {category_name} not available in {hou.applicationVersionString()}")

    with raiser:
        container = pytest_houdini.fixtures.nodes._context_container(category)
        assert container.type() == expected

        container.destroy()


def test_create_temp_node(pytester: pytest.Pytester) -> None:
    """Test the 'create_temp_node' fixture."""
    pytester.makepyfile("""
import hou

# Test the basic fixture behavior.
def test_create_temp_node(create_temp_node):
    assert hou.node("/obj").children() == ()

    result = create_temp_node(hou.node("/obj"), "geo", "TEST_NODE")

    assert hou.node("/obj").children() == (result, )

    assert result.name() == "TEST_NODE"
    assert result.parm("viewportlod") is not None


# Test if we manually destroy the node instead of relying on automatic cleanup.
# Also tests run_init_scripts arg passing.
def test_create_temp_node_manual_destroy(create_temp_node):
    assert hou.node("/obj").children() == ()

    result = create_temp_node(hou.node("/obj"), "geo", "TEST_MANUAL_NODE", run_init_scripts=False)

    assert hou.node("/obj").children() == (result, )

    assert result.name() == "TEST_MANUAL_NODE"
    assert result.parm("viewportlod") is None

    result.destroy()


# Test using the fixture to create multiple nodes.
def test_create_temp_node_multiple(create_temp_node):
    assert hou.node("/obj").children() == ()

    result1 = create_temp_node(hou.node("/obj"), "geo", "TEST_NODE1")
    result2 = create_temp_node(hou.node("/obj"), "null", "TEST_NODE2")

    assert hou.node("/obj").children() == (result1, result2)


# Sentinel test to ensure that the test code is run in-process and that things
# are being properly cleaned up.
def test_sentinel():
    hou.node("/obj").createNode("geo", "SENTINEL")

""")
    result = pytester.runpytest()

    result.assert_outcomes(passed=4)

    assert hou.node("/obj").children() == (hou.node("/obj/SENTINEL"),)


def test_create_context_container(pytester: pytest.Pytester) -> None:
    """Test the 'create_context_node' fixture."""
    pytester.makepyfile("""
import hou

# Test the basic fixture behavior.
def test_create_context_container(create_context_container):
    container1 = create_context_container(hou.sopNodeTypeCategory())
    container2 = create_context_container(hou.ropNodeTypeCategory())

    assert container1 in hou.node("/obj").children()
    assert container2 in hou.node("/out").children()
    container2.destroy()
""")
    result = pytester.runpytest()

    result.assert_outcomes(passed=1)

    assert hou.node("/obj").children() == (hou.node("/obj/SENTINEL"),)


def test_lop_test_node(pytester: pytest.Pytester, shared_datadir: Path) -> None:
    """Test the 'lop_test_node' fixture."""
    test_hip = shared_datadir / "test_nodes.hiplc"

    pytester.makepyfile(f"""
import hou

hou.hipFile.load("{test_hip.as_posix()}", ignore_load_warnings=True)

def test_lop_test_node(lop_test_node):
    target_node = hou.node("/stage/test_lop_test_node")

    assert target_node is not None
    assert target_node == lop_test_node

""")
    result = pytester.runpytest()

    result.assert_outcomes(passed=1)


def test_parametrized_node_names(pytester: pytest.Pytester, shared_datadir: Path) -> None:
    """Test to ensure node names are correct when using fixtures along with parametrized tests.

    The test nodes will be found according to the original name,
    test_obj_test_node_func, instead of test_obj_test_node_func[True|False].
    """
    test_hip = shared_datadir / "test_nodes.hiplc"

    pytester.makepyfile(f"""
import pytest

import hou

hou.hipFile.load("{test_hip.as_posix()}", ignore_load_warnings=True)

@pytest.mark.parametrize("extra_parm", (True, False))
def test_obj_test_node_func(obj_test_node, extra_parm, request):
    target_node = hou.node("/obj/test_obj_test_node_func")

    assert target_node is not None
    assert target_node == obj_test_node

""")
    result = pytester.runpytest()
    result.assert_outcomes(passed=2)


def test_obj_test_node(pytester: pytest.Pytester, shared_datadir: Path) -> None:
    """Test the 'obj_test_node' fixture."""
    test_hip = shared_datadir / "test_nodes.hiplc"

    pytester.makepyfile(f"""
import hou

hou.hipFile.load("{test_hip.as_posix()}", ignore_load_warnings=True)


class TestNodes:
    def test_full_name(self, obj_test_node):
        target_node = hou.node("/obj/TestNodes_full_name")

        assert target_node is not None
        assert target_node == obj_test_node

    def test_nested_name(self, obj_test_node):
        target_node = hou.node("/obj/TestNodes/nested_name")

        assert target_node is not None
        assert target_node == obj_test_node

    def test_only_class_name(self, obj_test_node):
        target_node = hou.node("/obj/TestNodes")
        assert target_node == obj_test_node

class TestLowerNodes:
    def test_full_name(self, obj_test_node):
        target_node = hou.node("/obj/testlowernodes_full_name")

        assert target_node is not None
        assert target_node == obj_test_node

    def test_nested_name(self, obj_test_node):
        target_node = hou.node("/obj/testlowernodes/nested_name")

        assert target_node is not None
        assert target_node == obj_test_node

    def test_only_class_name(self, obj_test_node):
        target_node = hou.node("/obj/testlowernodes")
        assert target_node == obj_test_node

def test_obj_test_node_func(obj_test_node):
    target_node = hou.node("/obj/test_obj_test_node_func")

    assert target_node is not None
    assert target_node == obj_test_node


def test_no_matching(obj_test_node):
    pass

""")
    result = pytester.runpytest()
    result.assert_outcomes(passed=7, errors=1)


def test_obj_test_geo(pytester: pytest.Pytester, shared_datadir: Path) -> None:
    """Test the 'obj_test_geo' fixture."""
    test_hip = shared_datadir / "test_nodes.hiplc"

    pytester.makepyfile(f"""
import hou

hou.hipFile.load("{test_hip.as_posix()}", ignore_load_warnings=True)

def test_obj_test_geo_missing(obj_test_geo):
    pass

def test_obj_test_geo_not_sop(obj_test_geo):
    pass

def test_obj_test_geo(obj_test_geo):
    target_node = hou.node('/obj/test_obj_test_geo/TARGET')

    assert obj_test_geo.sopNode() == target_node
    assert obj_test_geo.isReadOnly()

""")
    result = pytester.runpytest()

    result.assert_outcomes(passed=1, errors=2)


def test_obj_test_geo_copy(pytester: pytest.Pytester, shared_datadir: Path) -> None:
    """Test the 'obj_test_geo_copy' fixture."""
    test_hip = shared_datadir / "test_nodes.hiplc"

    pytester.makepyfile(f"""
import hou

hou.hipFile.load("{test_hip.as_posix()}", ignore_load_warnings=True)

def test_obj_test_geo_copy(obj_test_geo_copy):
    target_node = hou.node('/obj/test_obj_test_geo_copy/TARGET')

    assert obj_test_geo_copy.sopNode() is None
    assert not obj_test_geo_copy.isReadOnly()
    assert obj_test_geo_copy.intrinsicValue("pointcount") == target_node.geometry().intrinsicValue("pointcount")

""")
    result = pytester.runpytest()

    result.assert_outcomes(passed=1)


def test_out_test_node(pytester: pytest.Pytester, shared_datadir: Path) -> None:
    """Test the 'out_test_node' fixture."""
    test_hip = shared_datadir / "test_nodes.hiplc"

    pytester.makepyfile(f"""
import hou

hou.hipFile.load("{test_hip.as_posix()}", ignore_load_warnings=True)

def test_out_test_node(out_test_node):
    target_node = hou.node("/out/test_out_test_node")

    assert target_node is not None
    assert target_node == out_test_node

""")
    result = pytester.runpytest()

    result.assert_outcomes(passed=1)
