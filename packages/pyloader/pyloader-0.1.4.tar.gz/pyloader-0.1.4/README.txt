pyloader
===========

Load python attributes from strings

JSON Format
-----------

pyloader uses a JSON-serializable format for the canonical
(serializable) form of python objects::

 {'foo': # (arbitrary) object name,
  {'args': ['positional', 'arguments'],
   'kwargs': {'keyword': 'arguments},
   'path': 'dotted.or.file.path:ObjectName'},
  'bar': ... } # etc 

Objects are instantiated like::

 ObjectName(*args, **kwargs)

In the case that the object is not to be instantiated (e.g. a
standalone function, ``args`` and ``kwargs`` will either not be
present or will be None (``null`` in JSON).


INI Format
----------

pyloader also features an INI format which is translated to the JSON
Format but adds a few convenience features.  A simple object is
expressed as::

 [foo:dotted.or.file.path:ObjectName]
 . = positional, arguments
 keyword = arguments

``.`` expresses positional arguments which is a comma-separated
list. The remaining (key, value) pairs become keyword arguments. The
section name contains the object name (e.g. ``foo``) followed by a
``:`` followed by a loading path.  Like JSON, a dotted path or a file
path may be used. In addition, other (pluggable) loading paths are
available:

- override loader: you can use a section name like ``[foo:bar]`` to
  override variables from the ``bar`` object with variables from
  ``foo``::

   [foo:bar]
   . = cats, dogs
   type = count

   [bar:%(here)s/some/path.py:MyObject]
   . = elephants
   type = concatenate

  The above results in a JSON blob for foo like::

   {'foo': {'args': ['elephants', 'cats', 'dogs'],
            'kwargs': {'type': 'concatenate'},
            'path': '/location/of/ini/file/some/path.py:MyObject'}}

  ``args`` is extended. ``kwargs`` will be overridden.

- wrappers: in addition to the override pattern, you can also wrap an
  object::

   [foo:bar:baz]

  This will create an object, ``foo`` which wraps the object ``baz`` in
  by the pattern given by ``bar``.  In this case, ``bar`` is provided
  a special variable, `%(app)s`.

  You can also do::

   [foo:bar:hi,hello,x=1,y=2:%(here)/objects.py:MyClass]


In addition, .ini files may include other .ini files.  This allows for
encapsulation of intent of specific .ini files::

   [include:%(here)s/some/file.ini]

INI files have a few convenience variables:

- %(here)s : the location of the directory the .ini file lives in
- %(object)s : used for wrappers

Additional variables may be provided by the consumer.

Summary of .ini decorator syntax
--------------------------------

1. ``[foo:%(here)s/objects.py:MyClass]``: create object ``foo`` of type
   ``MyClass`` using arguments given from the section

2. ``[foo:bar]``: create object ``foo`` using the pattern from section
   ``bar`` but overriding any arguments in the ``bar`` section with
   those from this section 

3. ``[foo:bar:%(here)s/objects.py:MyClass]``: create object ``foo``
   which is an instance of ``MyClass`` wrapped in the object created by
   the ``bar`` pattern. ``bar`` is passed a special argument,
   ``%(object)s`` which is the instance of the wrapped object (the
   ``MyClass`` instance). Internally, the wrapped object is known by
   the whole section name (``foo:bar:%(here)s/objects.py:MyClass``). The 
   arguments in this section apply to ``MyClass(...)``

4. ``[foo:bar:app=%(object)s,value=1:%(here)s/objects.py:MyClass]``:
   the same as 3. but override the values in the ``bar`` section with
   ``app=%(object)s`` and ``value=1``

Section Name Syntax
-------------------

- *[name:resource]* : create an object named *name* , where resource
  is either a section name or a *path* as described in `JSON Format`_ .
  In the case where *resouce* is another section name, the options
  will overide the options given in the *resource* section and a new
  object named *name* will be created.  In the case where *section* is
  a path, an object will be created as given by the *path* with the
  given options.
- *[name:decorator:resource]* : create an object named *name* where
  the object given by *resource* is passed to *decorator*. Overrides
  and loading is as described for *[name:reource]* . An anonymous
  object is created of the whole section name for the wrapped
  object. So this form results in two sections for the `JSON Format`_ .
  *decorator* is a section in the same namespace as *name*.
- *[name:decorator:overrides:resource]* : similar to
  *[name:decorator:resource]* , but apply *overides* to the
  *decorator* section.  *overrides* is a string of the format
  ``foo,bar,fleem=5``.

----

Jeff Hammel
http://k0s.org/

