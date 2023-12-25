"""Initialize the pytest-houdini plugin."""

# Standard Library
from importlib.util import find_spec

# If Houdini is running then we can import our fixtures to expose.
if find_spec("hou"):
    from pytest_houdini.fixtures.hip_file import (
        clear_hip_file,
        load_module_test_hip_file,
        set_test_frame,
    )
    from pytest_houdini.fixtures.nodes import (
        create_temp_node,
        obj_test_geo,
        obj_test_geo_copy,
        obj_test_node,
        out_test_node,
    )
    from pytest_houdini.fixtures.other import remove_abstract_methods
    from pytest_houdini.fixtures.shelf_tools import exec_shelf_tool_script
    from pytest_houdini.fixtures.soho import patch_soho
    from pytest_houdini.fixtures.ui import (
        mock_hdefereval,
        mock_hou_qt,
        mock_hou_ui,
        set_ui_available,
    )
