pipsy
======

.. image:: https://travis-ci.org/tpyo/pipsy.svg?branch=master
    :target: https://travis-ci.org/tpyo/pipsy

A Python 3 tool to check for pypi package updates and security-related changes

Installation
^^^^^^^^^^^^^^^^^^
.. code::

    pip install pipsy

Usage
^^^^^^^^^^^^^^^^^^
**Check all installed packages**

.. code::

    pipsy

**Check specific packages**

.. code::

    pipsy Django requests pip

**Check change logs**

.. code::

    pipsy -c

**Output JSON**

.. code::

    pipsy -j Django requests
