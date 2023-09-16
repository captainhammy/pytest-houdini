=============
Miscellaneous
=============

``pytest-houdini`` also provides some other, more general fixtures that while perhaps not explicitly for Houdini are
useful for testing.

remove_abstract_methods
-----------------------

The ``remove_abstract_methods`` fixture is used to temporarily remove an object's abstract methods.

Consider the following class definition with an abstract method and a concrete method which we want to test. Rather than
creating a subclass which implements any abstract methods just for testing the non-abstract methods, we can use the
fixture to remove them during the test so that the object can be instantiated and the concrete method called.

.. code-block:: python

    class TestClass(metaclass=abc.ABCMeta):

        @abc.abstractmethod
        def bar(self):
            pass

        def get_foo(self):
            return "foo"


    def test_get_foo(remove_abstract_methods):
        remove_abstract_methods(TestClass)

        c = TestClass()
        assert c.get_foo() == "foo"

Without this we would hit a ``TypeError`` due to the abstract method.

.. code-block:: python

    def test_get_foo():
        c = TestClass()
        assert c.get_foo() == "foo"


    TypeError: Can't instantiate abstract class TestClass with abstract method bar
