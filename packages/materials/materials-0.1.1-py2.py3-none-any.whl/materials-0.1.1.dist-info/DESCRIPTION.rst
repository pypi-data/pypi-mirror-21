materials
=========

|Build Status| |codecov| |Code Health| |PyPi Version| |GitHub stars|

materials is a database of physical and chemical data, possibly with
temperature dependence, of various more or less common materials. All
data are given in SI units.

For example, to plot the density of various materials between 274 and
370 K you can do

.. code:: python

    import materials
    import matplotlib.pyplot as plt
    import numpy


    T = numpy.linspace(274.0, 370.0, num=100)

    rho_air = materials.air.density(T)
    rho_argon = materials.argon.density(T)
    rho_copper = materials.copper.density(T)
    rho_water = materials.water.density(T)

    plt.semilogy(T, rho_copper, label='copper')
    plt.semilogy(T, rho_water, label='water')
    plt.semilogy(T, rho_argon, label='argon')
    plt.semilogy(T, rho_air, label='air')

    plt.title('densities')
    plt.xlabel('temperature (K)')
    plt.ylabel('density (kg/m^3)')
    plt.legend()

    plt.show()

.. figure:: https://nschloe.github.io/materials/density.png
   :alt: 

Installation
~~~~~~~~~~~~

materials is `available from the Python Package
Index <https://pypi.python.org/pypi/materials/>`__, so simply type

::

    pip install -U materials

to install or upgrade.

Testing
~~~~~~~

To run the materials unit tests, check out this repository and type

::

    pytest

Distribution
~~~~~~~~~~~~

To create a new release

1. bump the ``__version__`` number,

2. publish to PyPi and GitHub:

   ::

       make publish

License
~~~~~~~

materials is published under the `MIT
license <https://en.wikipedia.org/wiki/MIT_License>`__.

.. |Build Status| image:: https://travis-ci.org/nschloe/materials.svg?branch=master
   :target: https://travis-ci.org/nschloe/materials
.. |codecov| image:: https://codecov.io/gh/nschloe/materials/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/nschloe/materials
.. |Code Health| image:: https://landscape.io/github/nschloe/materials/master/landscape.png
   :target: https://landscape.io/github/nschloe/materials/master
.. |PyPi Version| image:: https://img.shields.io/pypi/v/materials.svg
   :target: https://pypi.python.org/pypi/materials
.. |GitHub stars| image:: https://img.shields.io/github/stars/nschloe/materials.svg?style=social&label=Star&maxAge=2592000
   :target: https://github.com/nschloe/materials


