=====================
Supporting Test Tools
=====================

context_container
-----------------

The ``pytest_houdini.tools.context_container`` context manager provides an appropriate parent node (container) for which
you can create a child node of a particular type. Pass the node type category of the type you wish to create
and use the returned node to create a node under.

.. code-block:: python

    with context_container(hou.sopNodeTypeCategory()) as container:
        container.createNode("box")

    # Attempting to access 'container' will result in a hou.ObjectWasDeleted exception.

A new node of the container type will always be created. Unless specified when the
container node is created, it will be destroyed after the end of the scope.


.. code-block:: python

    with context_container(hou.sopNodeTypeCategory(), destroy=False) as container:
        container.createNode("box")

    # 'container' is not destroyed and can still be accessed


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
