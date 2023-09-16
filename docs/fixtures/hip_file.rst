Hip File Fixtures
=================

``pytest-houdini`` contains a number of fixtures designed to make running tests with hip files easier and to
ensure the session state is less dependent on previous tests.

clear_hip_file
--------------

The ``clear_hip_file`` fixture will clear the current session before and after test running, ensuring that the scene is
clean and as stateless as possible from previous tests.


load_module_test_hip_file
-------------------------

The ``load_module_test_hip_file`` fixture will load a test hip file with the same name as the running module.  It
supports .hip, .hiplc, and .hipnc type files (in that order). The hip file must be under a **data/** directory which is
a sibling of of test file. For this package, looking at the tests for the fixtures, we can see that we have a matching
hip file for ``test_nodes.py`` (``test_nodes.hiplc``).

.. code-block::

    $ tree tests/fixtures/
    tests/fixtures/
    ├── data
    │ ├── test_load_module_test_hip_file.hiplc
    │ ├── test_nodes.hiplc    <-- Matching hip file
    │ └── test_shelf_files.shelf
    ├── __init__.py
    ├── test_hip_file.py
    ├── test_nodes.py    <-- Test File
    ├── test_shelf_tools.py
    ├── test_soho.py
    └── test_ui.py

The fixture will also clear the hip file after the tests are completed.

As this is a **module** level fixture, to use it ensure you've added the following at the top of the test file:

.. code-block:: python

    pytestmark = pytest.mark.usefixtures("load_module_test_hip_file")


In the event the fixture cannot find a matching file, the raised ``RuntimeError`` will contain a list of all the paths
which were tried:

.. code-block:: python

    RuntimeError: Could not find a valid test hip: {test_file_dir}/data/{test_file_name}{.hip,.hiplc,.hipnc}


set_test_frame
--------------

The ``set_test_frame`` fixture allows you to set the current frame to a specific value for testing and then restores it
to the the frame **before** the test began once the test is completed.

Consider the following example where we will say that the frame before the test is run is set to **1001**.

.. code-block:: python

    def test_func(set_test_frame):
        hou.setFrame(1002)
        assert hou.frame() == 1002
        set_test_frame(1003)
        assert hou.frame() == 1003
        # Do other tests which rely on the frame being set to the 1003.

After ``test_func`` has completed, the current frame will be restored to the value **before** the
test was executed with the fixture: **1001**
