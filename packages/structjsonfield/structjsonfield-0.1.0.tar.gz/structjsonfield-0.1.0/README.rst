=============================
Django Structured JSONField
=============================

.. image:: https://badge.fury.io/py/structjsonfield.svg
    :target: https://badge.fury.io/py/structjsonfield

.. image:: https://travis-ci.org/tleguijt/structjsonfield.svg?branch=master
    :target: https://travis-ci.org/tleguijt/structjsonfield

.. image:: https://codecov.io/gh/tleguijt/structjsonfield/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/tleguijt/structjsonfield

Adding more structure to JSONFields

Documentation
-------------

The full documentation is at https://structjsonfield.readthedocs.io.

Quickstart
----------

Install Django Structured JSONField::

    pip install structjsonfield

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'structjsonfield',
        ...
    )

Use the StructJSONField in your form

.. code-block:: python

    from structjsonfield import StructJSONField


    ingredients = StructJSONField(
        structure={
            'name': forms.CharField(label=_('Name')),
            'amount': forms.CharField(label=_('Amount')),
            'units': forms.CharField(label=_('Units'))
        })

Prerequisites
-------------

* Make sure you have jQuery loaded in your template
* Make sure you load the necessary form media (js + css)

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox
