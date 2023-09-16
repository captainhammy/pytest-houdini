"""Test the pytest_houdini.fixtures.nodes module."""

# Standard Library
import importlib

# pytest-houdini
import pytest_houdini.fixtures.nodes

importlib.reload(pytest_houdini.fixtures.nodes)

pytest_plugins = ["pytester"]


# Tests


def test_obj_test_node(pytester, shared_datadir):
    """Test the 'obj_test_node' fixture."""
    test_hip = shared_datadir / "test_nodes.hiplc"

    pytester.makepyfile(
        f"""
import hou

hou.hipFile.load("{test_hip.as_posix()}")


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

"""
    )
    result = pytester.runpytest()

    result.assert_outcomes(passed=7, errors=1)


def test_obj_test_geo(pytester, shared_datadir):
    """Test the 'obj_test_geo' fixture."""
    test_hip = shared_datadir / "test_nodes.hiplc"

    pytester.makepyfile(
        f"""
import hou

hou.hipFile.load("{test_hip.as_posix()}")

def test_obj_test_geo_missing(obj_test_geo):
    pass

def test_obj_test_geo_not_sop(obj_test_geo):
    pass

def test_obj_test_geo(obj_test_geo):
    target_node = hou.node('/obj/test_obj_test_geo/TARGET')

    assert obj_test_geo.sopNode() == target_node
    assert obj_test_geo.isReadOnly()

"""
    )
    result = pytester.runpytest()

    result.assert_outcomes(passed=1, errors=2)


def test_obj_test_geo_copy(pytester, shared_datadir):
    """Test the 'obj_test_geo_copy' fixture."""
    test_hip = shared_datadir / "test_nodes.hiplc"

    pytester.makepyfile(
        f"""
import hou

hou.hipFile.load("{test_hip.as_posix()}")

def test_obj_test_geo_copy(obj_test_geo_copy):
    target_node = hou.node('/obj/test_obj_test_geo_copy/TARGET')

    assert obj_test_geo_copy.sopNode() is None
    assert not obj_test_geo_copy.isReadOnly()
    assert obj_test_geo_copy.intrinsicValue("pointcount") == target_node.geometry().intrinsicValue("pointcount")

"""
    )
    result = pytester.runpytest()

    result.assert_outcomes(passed=1)


def test_out_test_node(pytester, shared_datadir):
    """Test the 'out_test_node' fixture."""
    test_hip = shared_datadir / "test_nodes.hiplc"

    pytester.makepyfile(
        f"""
import hou

hou.hipFile.load("{test_hip.as_posix()}")

def test_out_test_node(out_test_node):
    target_node = hou.node("/out/test_out_test_node")

    assert target_node is not None
    assert target_node == out_test_node

"""
    )
    result = pytester.runpytest()

    result.assert_outcomes(passed=1)
