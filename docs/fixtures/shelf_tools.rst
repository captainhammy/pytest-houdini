===========
Shelf Tools
===========

There is not an easy programmatic way to execute various Houdini UI elements such as shelf tools so ``pytest-houdini``
attempts to provide some tooling to help with this.

exec_shelf_tool_script
----------------------

The ``exec_shelf_tool_script`` fixture allows you to execute a shelf tool's script code section.

The fixture is a **callable** which requires the name of the tool, as well as a dictionary representing the ``kwargs``
that would be passed to the shelf tool by Houdini.

In order for this fixture to work, the shelf tool must already be loaded in the Houdini session.

Consider the following simple tool definition where the execution sets a value in the kwargs dict:

.. code-block:: xml

    # my_tool.shelf

    <?xml version="1.0" encoding="UTF-8"?>
    <shelfDocument>
      <tool name="my_tool" label="My Tool" icon="PLASMA_App">
        <script scriptType="python"><![CDATA[kwargs["result"] = True]]></script>
      </tool>
    </shelfDocument>

We can execute this tool by passing its name along with a dictionary and test that it ran by checking that it set the
*result* value to ``True``.

.. code-block::

    def test_tool(exec_shelf_tool_script):
        # Ensure the tool is loaded in Houdini so that we can access it.
        hou.shelves.loadFile("/path/to/my_tool.shelf")

        test_kwargs = {"result": False}

        exec_shelf_tool_script("my_tool", test_kwargs)

        assert test_kwargs["result"]
