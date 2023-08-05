.. MCres

:Name: MCres
:Website: https://github.com/ceyzeriat/MCres
:Author: Guillaume Schworer
:Version: 0.2beta

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://github.com/ceyzeriat/MCres/blob/master/LICENSE.txt

Blah
It is released under the MIT license.

.. code-block:: python

    import MCres

#.. image:: https://raw.githubusercontent.com/ceyzeriat/MCres/master/img/obs_ex.png
#   :align: center

Documentation
=============

Refer to this page, http://pythonhosted.org/MCres/MCres.html


Requirements
============

MCres requires the following Python packages:

* NumPy, Scipy: for basic numerical routines
* astropy.io.fits: for angle units
* corner: for plotting
* matplotlib: for plotting
* time: for basic stuff

MCres is tested on Linux and Python 2.7 only, but should cross-plateform without too many issues.

Installation
============

If you use anaconda, the easiest and fastest way to get the package up and running is to
install MCres using `conda <http://conda.io>`_::

  $ conda install MCres --channel MCres

You can also install MCres from PyPI using pip, given that you already
have all the requirements::

  $ pip install MCres

You can also download MCres source from GitHub and type::

  $ python setup.py install

Contributing
============

Code writing
------------

Code contributions are welcome! Just send a pull request on GitHub and we will discuss it. In the `issue tracker`_ you may find pending tasks.

Bug reporting
-------------

If you think you've found one please refer to the `issue tracker`_ on GitHub.

.. _`issue tracker`: https://github.com/ceyzeriat/MCres/issues

Additional options
------------------

You can either send me an e-mail or add it to the issues/wishes list on GitHub.

Citing
======

If you use MCres on your project, please
`drop me a line <mailto:{my first name}.{my family name}@obspm.fr>`, you will get fixes and additional options earlier.

License
=======

MCres is released under the MIT license, hence allowing commercial use of the library. Please refer to the LICENSE.txt file.
