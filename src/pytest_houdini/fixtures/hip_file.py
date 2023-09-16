"""Fixtures related to hip files."""

# Future
from __future__ import annotations

# Standard Library
from typing import TYPE_CHECKING, Callable, Union

# Third Party
import pytest

# Houdini
import hou

if TYPE_CHECKING:
    from collections.abc import Generator

# Fixtures


@pytest.fixture
def clear_hip_file() -> Generator[None, None, None]:
    """Fixture to clear the current hip file before and after test running."""
    hou.hipFile.clear(suppress_save_prompt=True)

    yield

    hou.hipFile.clear(suppress_save_prompt=True)


@pytest.fixture(scope="module")
def load_module_test_hip_file(
    request: pytest.FixtureRequest,
) -> Generator[None, None, None]:
    """Load a test hip file with the same name as the running module.

    Supports .hip, .hiplc, and .hipnc type files.

    The file must be under a data/ directory which is a sibling of the test file.

    The fixture will clear the hip file after the tests are completed.

    Example:
        Place the following line at the top of the test module::

            pytestmark = pytest.mark.usefixtures("load_module_test_hip_file")

    """
    test_file_path = request.path

    data_dir = test_file_path.parent / "data"

    hip_extensions = (".hip", ".hiplc", ".hipnc")

    for hip_ext in hip_extensions:
        # Look for a file with the test module's name and accompanying hip ext.
        test_file_name = test_file_path.with_suffix(hip_ext).name

        test_file_path = data_dir / test_file_name

        if test_file_path.is_file():
            break

    # We didn't find a matching file so raise an exception indicating no file could be found
    # and include the various paths we tried.
    else:
        raise RuntimeError(
            f"Could not find a valid test hip: {data_dir}/{test_file_path.stem}{{{','.join(hip_extensions)}}}"
        )

    hou.hipFile.load(
        test_file_path.as_posix(), suppress_save_prompt=True, ignore_load_warnings=True
    )

    yield

    hou.hipFile.clear(suppress_save_prompt=True)


@pytest.fixture
def set_test_frame() -> Generator[Callable, None, None]:
    """Fixed to set a frame for testing, restoring the previous one after completion.

    >>> def test_func(set_test_frame):
    ...    set_test_frame(1001)
    ...    # Do test things

    """
    current_frame = hou.frame()

    def _set_test_frame(frame: Union[float, int]) -> None:
        hou.setFrame(frame)

    yield _set_test_frame

    hou.setFrame(current_frame)
