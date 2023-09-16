==
UI
==

``pytest-houdini`` contains a number of useful fixtures for mocking UI related modules for testing.

mock_hdefereval
---------------

The ``mock_hdefereval`` fixture mocks the ``hdefereval`` module which can have issues is in non-graphical Houdini.

The ``mock_hdefereval`` fixture provides a ``MagicMock`` object representing the ``hdefereval`` module. This object has
been monkeypatched into ``sys.modules`` for the duration of the test.

If you need to test code which uses this module you'll want to use this fixture as importing the module in non-graphical
Houdini (hython) will result in an ``ImportError`` due to the UI not being available.

.. code-block::

    def my_func():
        print("I'm deferred!")

    def run_my_func_deferred():
        hdefereval.executeDeferred(my_func)

    def test_run_my_func_deferred(mock_hdefereval):
        run_my_func_deferred()

        mock_hdefereval.executeDeferred.assert_called_with(my_func)

        import hdefereval
        assert hdefereval == mock_hdefereval


mock_hou_qt
-----------

The ``mock_hou_qt`` fixture mocks the ``hou.qt`` module which is not available in non-graphical Houdini.

It will monkeypatch in and return a ``MagicMock`` object which represents the ``hou.qt`` module.

The temporary ``hou.qt`` object is removed after the test is completed.

.. code-block::

    def get_icon(icon_name):
        return hou.qt.Icon(icon_name)

    def test_get_icon(mock_hou_qt):
        icon = get_icon("SOP_box")

        assert icon == mock_hou_qt.Icon.return_value
        assert hou.qt == mock_hou_qt

mock_hou_ui
-----------

The ``mock_hou_ui`` fixture mocks the ``hou.ui`` module which is not available in non-graphical Houdini.

It will monkeypatch in and return a ``MagicMock`` object which represents the ``hou.ui`` module.

The temporary ``hou.ui`` object is removed after the test is completed.

.. code-block::

    def output_message(message):
        hou.ui.displayMessage(message)
        hou.ui.setStatusMessage(message)

    def test_output_message(mock_hou_ui):
        output_message("This is a message")

        mock_hou_ui.displayMessage.assert_called()
        mock_hou_ui.setStatusMessage.assert_called()

        assert hou.ui == mock_hou_ui

set_ui_available
----------------

The ``set_ui_available`` fixtures forces the ``hou.isUIAvailable()`` function to return True.

.. code-block:: python

    def test_ui_available(set_ui_available):
        assert hou.isUIAvailable()

