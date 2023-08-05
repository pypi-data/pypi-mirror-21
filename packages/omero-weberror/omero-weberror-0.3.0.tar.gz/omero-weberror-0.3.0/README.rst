.. image:: https://travis-ci.org/openmicroscopy/omero-weberror.svg?branch=master
    :target: https://travis-ci.org/openmicroscopy/omero-weberror

.. image:: https://badge.fury.io/py/omero-weberror.svg
    :target: https://badge.fury.io/py/omero-weberror


OMERO.weberror
==============
OMERO.web app that helps testing errors, notification logic etc.

Requirements
============

* OMERO 5.2.6 or newer.

Installing from PyPI
====================

This section assumes that an OMERO.web is already installed.

Install the app using `pip <https://pip.pypa.io/en/stable/>`_:

::

    $ pip install omero-weberror

Add weberror custom app to your installed web apps:

::

    $ bin/omero config append omero.web.apps '"omero_weberror"'

Now restart OMERO.web as normal.

**Warning**:

OMERO.weberror version 0.2.x requires OMERO.web **5.2.6 or newer**.
This is due to Django Framework compatibility and to a required package reorganization in OMERO.weberror in version 0.2.0 so the application can be distributed from Python Package Index `PyPI <https://pypi.python.org/pypi>`_.


License
-------

OMERO.weberror is released under the AGPL.

Copyright
---------

2016-2017, The Open Microscopy Environment
