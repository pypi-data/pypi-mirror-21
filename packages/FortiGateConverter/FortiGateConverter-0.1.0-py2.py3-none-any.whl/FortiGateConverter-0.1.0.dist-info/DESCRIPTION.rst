=============================
FortiGateConverter
=============================

.. image:: https://badge.fury.io/py/FortiGateConverter.svg
    :target: https://badge.fury.io/py/FortiGateConverter

.. image:: https://travis-ci.org/zhangdunxing/FortiGateConverter.svg?branch=master
    :target: https://travis-ci.org/zhangdunxing/FortiGateConverter

.. image:: https://codecov.io/gh/zhangdunxing/FortiGateConverter/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/zhangdunxing/FortiGateConverter

Help to migrate configuration between FGTs.

Documentation
-------------

The full documentation is at https://FortiGateConverter.readthedocs.io.

Quickstart
----------

Install FortiGateConverter::

    pip install FortiGateConverter

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'fortigateconverter.apps.FortigateconverterConfig',
        ...
    )

Add FortiGateConverter's URL patterns:

.. code-block:: python

    from fortigateconverter import urls as fortigateconverter_urls


    urlpatterns = [
        ...
        url(r'^', include(fortigateconverter_urls)),
        ...
    ]

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

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage




History
-------

0.1.0 (2017-04-20)
++++++++++++++++++

* First release on PyPI.


