metaset
=======

This package provides a collection that is basically a "dict of sets", named MetaSet.

.. image:: https://travis-ci.org/Polyconseil/metaset.svg?branch=master
    :alt: Build status

.. image:: https://img.shields.io/pypi/pyversions/metaset.svg
    :alt: Supported Python versions

.. image:: https://img.shields.io/pypi/wheel/metaset.svg
    :alt: Wheel status

.. image:: https://img.shields.io/pypi/l/metaset.svg
    :alt: License

Links
-----

- Package on `PyPI`_: http://pypi.python.org/pypi/metaset/
- Source on `GitHub <http://github.com/>`_: http://github.com/Polyconseil/metaset/
- Build on `Travis CI <http://travis-ci.org/>`_: http://travis-ci.org/lionel-panhaleux/metaset/

Quickstart
----------

Install the package from PyPI_, using pip:

.. _PyPI: http://pypi.python.org/pypi/metaset/

.. code-block:: sh

    pip install metaset


Or from GitHub:

.. code-block:: sh

    git clone git://github.com/Polyconseil/metaset.git

Import it in your code:

.. code-block:: python

    >>> from metaset import MetaSet

Usage is quite straight forward,
basic set operations are supported via the binary operators ``+`` ``-`` ``|`` ``^``.

.. code-block:: python

    >>> from pprint import pprint
    >>> pprint(MetaSet(a={1, 2}, b={3}) | MetaSet(b={4}, c={5}))
    {'a': {1, 2}, 'b': {3, 4}, 'c': {5}}

Django Postgres
---------------

A custom Django field is available.
Note it is only available with ``PostgreSQL≥9.4`` and ``Psycopg2≥2.5.4``, as it is stored as a ``JSONB`` column.
It is quite straightforward:

.. code-block:: python

    >>> from metaset.django_field import MetaSetField
    >>> from django.db import models        # doctest: +SKIP

    >>> class MyModel(models.Model):        # doctest: +SKIP
            mset = MetaSetField()           # doctest: +SKIP

It is compatible with the following versions:

- Django 1.7, Python 2.7, 3.4 (requires `jsonfield`_)
- Django 1.8, Python 2.7, 3.5 (requires `jsonfield`_)
- Django 1.9, Python 2.7, 3.5
- Django 1.10, Python 2.7, 3.5

Note when you use `Django>=1.9` you have access to `JSON-specific lookups`_ not available when using `jsonfield`_
on earlier versions:

.. code-block:: python

    >>> MyModel.objects.filter(mset__a__contains=[1, 2])            # doctest: +SKIP
    >>> MyModel.objects.filter(mset__a__contained_by=range(10))     # doctest: +SKIP
    >>> MyModel.objects.filter(mset__has_key='a')                   # doctest: +SKIP
    >>> MyModel.objects.filter(mset__has_keys=('a', 'b'))           # doctest: +SKIP
    >>> MyModel.objects.filter(mset__has_any_keys=('a', 'b'))       # doctest: +SKIP

.. _jsonfield: https://pypi.python.org/pypi/jsonfield
.. _JSON-specific lookups: https://docs.djangoproject.com/en/1.10/ref/contrib/postgres/fields/#containment-and-key-operations

Detailed considerations
-----------------------

They are two ways to consider the "dict of sets" notion,
differing on how you handle the empty values for keys.

The easiest idea is to consider that a key with no content is non-existent.
This is how the dictset_ package is implemented.

In this alternative implementation,
we chose to keep the empty keys as meaningful elements,
allowing for smart unions and intersections.

.. code-block:: python

    >>> pprint(MetaSet(a={1}) | MetaSet(a={2}, b=set()))
    {'a': {1, 2}, 'b': set()}

    >>> MetaSet(a={1}) & MetaSet(a={2}, b={3})
    {'a': set()}

So, beware of how empty-keys are handled,
and consider using dictset_ if it is a better match for your use case.
The behavior for subtraction and symmetric difference,
although sound on a mathematical point of view, may not be what you want.

.. code-block:: python

    >>> MetaSet(a={1}) - MetaSet(a={1})
    {'a': set()}

    >>> MetaSet(a={1}) ^ MetaSet(a={1})
    {'a': set()}

.. _dictset: https://code.google.com/archive/p/dictset/
