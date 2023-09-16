=====================
Supporting Test Tools
=====================



does_not_raise
--------------

The ``pytest_houdini.tools.does_not_raise`` function is a dummy context manager for testing.

You can use this to help parametrize tests which may or may not raise exceptions.

Consider the below test for a function which divides two values. As it does not
validate any of the values it will result in ``ZeroDivisionError`` if *value2* is 0. We
can use ``does_not_raise()`` in conjunction with ``pytest.raises(ZeroDivisionError)`` in order
to test a bunch of values and handle any expected exceptions.

.. code-block:: python

    def divider(value1, value2):
        return value1 / value2

    @pytest.mark.parametrize(
        "value, expected, tester",
        [
            (0, None, pytest.raises(ZeroDivisionError)),
            (3.0, 0.3333333333333333, does_not_raise()),
        ],
    )
    def test_divider(value, expected, tester):

        with tester:
            result = divider(1, value)

            assert result == expected

