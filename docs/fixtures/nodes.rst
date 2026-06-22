=====
Nodes
=====

create_temp_node
----------------

The :func:`~pytest_houdini.fixtures.nodes.create_temp_node` fixture can be used to create temporary testing nodes and not have to worry about
destroying them after the test is over. Additionally, it can be called multiple times to create many temporary nodes.

It supports a limited number of parameters to affect the node creation:

.. code-block:: python

    def _create(
        parent: hou.OpNode,
        node_type_name: str,
        node_name: str | None = None,
        *,
        run_init_scripts: bool = True
    ) -> hou.OpNode:
        """Function to create a test node that will be destroyed on cleanup.

        Args:
            parent: The parent to create the test node under.
            node_type_name: The node type to create.
            node_name: Optional node name.
            run_init_scripts: Whether to run the node initialization scripts.

        Return:
            The created test node.
        """

In the following example we create some temp nodes to test with.

.. code-block:: python

    def test_some_func(create_temp_node):
        node1 = create_temp_node(hou.node("/obj"), "geo", "TEST_NODE1", run_init_scripts=False)
        node2 = create_temp_node(hou.node("/obj"), "null", "TEST_NODE2")

        ... # do testing

After the test function is executed, the created nodes will both be destroyed.  If the test code itself
destroys a node, the :exc:`hou.ObjectWasDeleted` exception will be suppressed.


create_context_container
------------------------

The :func:`~pytest_houdini.fixtures.nodes.create_context_container` fixture  provides an appropriate parent node
(container) for which you can create a child node of a particular type. Pass the node type category of the type you wish
to create and use the returned node to create additional nodes under. The created parent node is destroyed after the test
finishes.

The callable fixture takes a :class:`hou.NodeTypeCategory`.

.. code-block:: python

    def test_some_func(create_context_container):
        container = create_context_container(hou.sopNodeTypeCategory())
        node = container.createNode("box")
        ... # do testing

.. list-table:: Container node types
    :header-rows: 1

    * - Context
      - Container Node Type
    * - Cop
      - CopNet/copnet
    * - Cop2
      - CopNet/img
    * - Dop
      - Object/dopnet
    * - Driver
      - Driver/subnet
    * - Lop
      - Lop/subnet
    * - Object
      - Object/subnet
    * - Shop
      - Shop/material
    * - Sop
      - Object/geo
    * - Top
      - Object/topnet
    * - Vop
      - Vop/subnet


Existing Test Node Fixtures
---------------------------

There are a number of convenience functions which can be used to automatically find test related nodes in the current
hip file based on the test name data.

The underlying tooling will inspect the :class:`pytest.FixtureRequest` object and construct a number of acceptable
node names/paths for the specific test and try to return one of those.  If a matching node cannot be found a
:exc:`~pytest_houdini.fixtures.exceptions.NoTestNodeError` is raised and the test will fail.

The node search order is as follows:
    - Node matching the exact test name
    - Node matching the class name + test name (minus "test\_" prefix for function name)
    - Node matching the class name / test name (minus "test\_" prefix for function name)
    - Node matching the class name

In the case of using the test class name, the class name component of the node name can match exactly or be lower case.

For example, a simple test function named **test_myfunc** would attempt to find a node named **test_myfunc** under the desired
parent node. In the example below this would be an Object node under "/obj".

.. code-block:: python

    def test_myfunc(obj_test_node):
        assert obj_test_node.path() == "/obj/test_myfunc"


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

In the event that no valid nodes could be provided, the raised :exc:`~pytest_houdini.fixtures.exceptions.NoTestNodeError`
will contain a list of all paths which were tried:

.. code-block:: python

    NoTestNodeError: Could not find any matching test nodes: /obj/test_none_args, /obj/TestMyFunc_none_args, /obj/testmyfunc_none_args, /obj/TestMyFunc/none_args, /obj/testmyfunc/none_args, /obj/TestMyFunc, /obj/testmyfunc


Basic Context Fixtures
^^^^^^^^^^^^^^^^^^^^^^

\*_test_node
''''''''''''

The ``*_test_node`` fixtures will attempt to find a test node under their specific contexts (as detailed above for **obj_test_node**)

The following contexts are currently provided:
    - /obj (:obj:`~pytest_houdini.fixtures.nodes.obj_test_node`)
    - /out (:obj:`~pytest_houdini.fixtures.nodes.out_test_node`)
    - /stage (:obj:`~pytest_houdini.fixtures.nodes.lop_test_node`)


Object Specific Fixtures
^^^^^^^^^^^^^^^^^^^^^^^^

obj_test_geo
''''''''''''

The :obj:`~pytest_houdini.fixtures.nodes.obj_test_geo` fixture will attempt to return the geometry of the display node of the found Object test node.

If the found test node (using :obj:`~pytest_houdini.fixtures.nodes.obj_test_node`) does not contain **SOP** nodes a :exc:`~pytest_houdini.fixtures.exceptions.TestNodeDoesNotContainSOPsError` is raised.

The returned :class:`hou.Geometry` object is **read only**.

.. code-block:: python

    def test_get_geo(obj_test_geo, obj_test_node):
        assert obj_test_geo.sopNode() == obj_test_node.displayNode()
        assert obj_test_geo.isReadOnly()


obj_test_geo_copy
'''''''''''''''''

The :obj:`~pytest_houdini.fixtures.nodes.obj_test_geo_copy` fixture is the same as :obj:`~pytest_houdini.fixtures.nodes.obj_test_geo` however the found geometry is copied/merged into a
new :class:`hou.Geometry` instance and is not **read only**.

.. code-block:: python

    def test_get_geo(obj_test_geo_copy):
        # There is no referenced SOP due to being a standalone hou.Geometry.
        assert obj_test_geo_copy.sopNode() is None
        assert not obj_test_geo_copy.isReadOnly()

