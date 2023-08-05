Python Arlo
-----------

.. image:: https://badge.fury.io/py/pyarlo.svg
    :target: https://badge.fury.io/py/pyarlo

.. image:: https://travis-ci.org/tchellomello/python-arlo.svg?branch=master
    :target: https://travis-ci.org/tchellomello/python-arlo

.. image:: https://coveralls.io/repos/github/tchellomello/python-arlo/badge.svg
    :target: https://coveralls.io/github/tchellomello/python-arlo

.. image:: https://img.shields.io/pypi/pyversions/pyarlo.svg
    :target: https://pypi.python.org/pypi/pyarlo


Python Arlo  is a library written in Python 2.7/3x that exposes the Netgear Arlo cameras as Python objects.

Installation
------------

.. code-block:: bash

    $ pip install pyarlo

    # Install latest development
    $ pip install \
        git+https://github.com/tchellomello/python-arlo@dev

Usage
-----

.. code-block:: python

    # list devices
    from pyarlo import PyArlo
    arlo  = PyArlo('foo@bar', 'secret')

    arlo.devices
    {'cameras': [<ArloCamera: Garage>,  <ArloCamera: Patio>,
      <ArloCamera: Front Door>, <ArloCamera: Patio Gate>]}

    # list all cameras
    arlo.cameras
    [<ArloCamera: Garage>, <ArloCamera: Patio>,
     <ArloCamera: Front Door>, <ArloCamera: Patio Gate>]

    # download latest snapshot image
    for camera in arlo.cameras:
        snapshot = '{0}.jpg'.format(camera.name)
        camera.download_snapshot(snapshot)
