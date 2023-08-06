=========
classical
=========

Convenience tools for working with Python classes.

Simplified subclassing:

::

    class MyClass:
        def __init__(self, *args, **kwargs):
            pass  # do whatever

    # subclass with presets
    MySubClass = partial_class(MyClass, 'MySubClass', arg1='value', arg2=4)

Various descriptors:
::

    class Thing:
        Red = PartialProperty(color='red')
        book = AutoProperty(has='pages')
        def __init__(self, color=None, has=None):
            self.color = color
            self.has = has

    Thing.Red  # is a subclass of Thing and is 'red'
    Thing.Red.book  # is an instance of Thing (and Thing.Red), is 'red' and has 'pages'


See the full documentation at http://classical.readthedocs.io/en/latest/


Installation
~~~~~~~~~~~~

::

    pip install classical


Testing
~~~~~~~

::

    make test

You may need to install ``[develop]`` extras to run tests


Generating docs
~~~~~~~~~~~~~~~

::

    make docs

You may need to install ``[develop]`` extras to generate docs
