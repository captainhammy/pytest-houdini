"""Test the pytest_houdini.fixtures.hip_file module."""

# Standard Library
import importlib
import shutil

# Third Party
import pytest

# pytest-houdini
import pytest_houdini.fixtures.hip_file

# Houdini
import hou

importlib.reload(pytest_houdini.fixtures.hip_file)

pytest_plugins = ["pytester"]


# Tests


def test_clear_hip_file(pytester):
    """Test the 'clear_hip_file' fixture."""

    pytester.makepyfile(
        """
import hou

def test_clear_hip_file(clear_hip_file, request):
    assert hou.node("/obj").children() == ()

    obj = hou.node("/obj")
    obj.createNode("null")

"""
    )

    # Create a node under /obj so there will be something there before the fixture
    # clears the hip file on setup.
    obj = hou.node("/obj")
    geo = obj.createNode("geo")

    # Run the test code.
    result = pytester.runpytest()

    result.assert_outcomes(passed=1)

    # Attempt to access the geom object we created.  This should fail as the node
    # was destroyed when the file was cleared.
    with pytest.raises(hou.ObjectWasDeleted):
        geo.path()

    # Ensure the null that was created during the test function was destroyed to
    # confirm that the file was cleared on cleanup.
    assert hou.node("/obj").children() == ()


@pytest.mark.parametrize("ext", (".hip", ".hiplc", ".hipnc", None))
def test_load_module_test_hip_file(pytester, ext, shared_datadir):
    """Test the 'load_module_test_hip_file' fixture."""

    data_dir = pytester.mkdir("data")

    expected_path = "untitled.hip"

    if ext is not None:
        hip_path = data_dir / f"test_load_module_test_hip_file{ext}"

        test_file = shared_datadir / "test_load_module_test_hip_file.hiplc"

        shutil.copy(test_file, hip_path)

        expected_path = hip_path.as_posix()

    pytester.makepyfile(
        f"""
import pytest

import hou

pytestmark = pytest.mark.usefixtures("load_module_test_hip_file")

def test_load_module_test_hip_file():
    assert hou.hipFile.path() == "{expected_path}"

"""
    )
    result = pytester.runpytest()

    if ext is None:
        result.assert_outcomes(errors=1)

    else:
        result.assert_outcomes(passed=1)


def test_set_test_frame(pytester):
    """Test the 'set_test_frame' fixture."""

    pytester.makepyfile(
        """
import hou

def test_set_test_frame(set_test_frame):
    set_test_frame(102)

    assert hou.frame() == 102

"""
    )

    hou.setFrame(101)

    assert hou.frame() == 101

    result = pytester.runpytest()

    assert hou.frame() == 101

    result.assert_outcomes(passed=1)
