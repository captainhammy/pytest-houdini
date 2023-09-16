=====
Nodes
=====

There are a number of convenience functions which can be used to automatically find test related nodes in the current
hip file based on the test name data.

The underlying tooling will inspect the ``pytest.FixtureRequest`` object and construct a number of acceptable
node names/paths for the specific test and try to return one of those.  If a matching node cannot be found a
``RuntimeError`` is raised and the test will fail.

The node search order is as follows:
    - Node matching the exact test name
    - Node matching the class name + test name (minus "test\_" prefix for function name)
    - Node matching the class name / test name (minus "test\_" prefix for function name)
    - Node matching the class name

In the case of using the test class name, the class name component of the node name can match exactly or be lower case.

For example, a simple test function named **test_myfunc** would attempt to find a node named **myfunc** under the desired
parent node. In the example below this would be an Object node under "/obj".

.. code-block:: python

    def test_myfunc(obj_test_node):
        assert obj_test_node.path() == "/obj/myfunc"


For the following test class it is a bit more complicated:

.. code-block:: python

    class TestMyFunc:

        def test_none_args(self, obj_test_node):
            pass

Again, we'll be using an Object node as the example.  So, what could a valid **obj_test_node** path be?  From above,
the possible nodes found (and their order of precedence) is as follows:

    - /obj/TestMyFunc_none_args
    - /obj/testmyfunc_none_args
    - /obj/TestMyFunc/none_args
    - /obj/testmyfunc/none_args
    - /obj/TestMyFunc
    - /obj/testmyfunc

In the event that no valid nodes could be provided, the raised ``RuntimeError`` will contain a list of all paths which
were tried:

.. code-block:: python

    RuntimeError: Could not find any matching test nodes: /obj/test_none_args, /obj/TestMyFunc_none_args, /obj/testmyfunc_none_args, /obj/TestMyFunc/none_args, /obj/testmyfunc/none_args, /obj/TestMyFunc, /obj/testmyfunc


obj_test_node
-------------

The ``obj_test_node`` fixture will attempt to find a test node under **/obj** (as detailed above in examples).

obj_test_geo
------------

The ``obj_test_geo`` fixture will attempt to return the geometry of the display node of the found Object test node.

If the found test node (using ``obj_test_node``) does not contain **SOP** nodes a ``RuntimeError`` is raised.

The returned ``hou.Geometry`` object is **read only**.

.. code-block:: python

    def test_get_geo(obj_test_geo, obj_test_node):
        assert obj_test_geo.sopNode() == obj_test_node.displayNode()
        assert obj_test_geo.isReadOnly()



obj_test_geo_copy
-----------------

The ``obj_test_geo_copy`` fixture is the same as ``obj_test_geo`` however the found geometry is copied/merged into a
new ``hou.Geometry`` instance and is not **read only**.

.. code-block:: python

    def test_get_geo(obj_test_geo_copy):
        # There is no referenced SOP due to being a standalone hou.Geometry.
        assert obj_test_geo_copy.sopNode() is None
        assert not obj_test_geo_copy.isReadOnly()

