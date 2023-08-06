=============================
django-atom
=============================

.. image:: https://badge.fury.io/py/django-atom.png
    :target: https://badge.fury.io/py/django-atom

.. image:: https://travis-ci.org/ad-m/django-atom.png?branch=master
    :target: https://travis-ci.org/ad-m/django-atom

A different stuff for Django to faster make a world a better place.

Documentation
-------------

The full documentation is at https://django-atom.readthedocs.org.

Quickstart
----------

Install django-atom::

    pip install django-atom

Then use it in a project::

    import atom

Extensions
----------

slugify
######
Example usage in ``settings.py`` add

.. code:: python

 AUTOSLUG_SLUGIFY_FUNCTION = 'atom.ext.slugify.slugifier.ascii_slugify'

Required ```unicode-slugify```, ```django-autoslug```.




History
-------

0.1.0 (2015-08-01)
++++++++++++++++++

* First release on PyPI.

0.2.0 (2015-08-04)
+++++++++++++++++

* Added AutocompleteChoiceFilter
* Add CSS-class settings for CrispyFormFilter
* Drop strict requirements for django-tinycontent

0.3.0 (2015-08-04)
+++++++++++++++++

* Split class to independent package to resolve dependencies issues

0.6.0 (2015-10-25)
+++++++++++++++++

* A lot

0.10.0 (2015-11-21)
+++++++++++++++++

* Add asci_slugifier
* Add absolute_import to crispy_forms

0.11.0 (2015-12-10)
+++++++++++++++++

* Fix support of dj19 by autocomplete_light API changes

0.12.0 (2016-12-4)
++++++++++++++++++

* Add ``atom.ext.guardian.tests.PermissionStatusMixin``


0.12.8 (2016-12-16)
+++++++++++++++++++

* Mark code as Python 3 compatible


