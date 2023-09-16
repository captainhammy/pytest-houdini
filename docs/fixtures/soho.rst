=============
Mantra / SOHO
=============

patch_soho
----------

The ``patch_soho`` fixture is a catch-all fixture for mocking various Mantra and SOHO modules.  It currently covers the
following modules via a singular named tuple with correspondingly named mock objects:

    - IFDapi
    - IFDframe
    - IFDhooks
    - IFDsettings
    - mantra
    - soho

For example, to test code that is run by Mantra, we could use this to mock a ``mantra.property()`` call:

.. code-block:: python

    def get_foo():
        return mantra.property("foo")

    def test_get_foo(patch_soho):
        patch_soho.mantra.property.return_value = 3

        assert get_foo() == 3
