perfplot
========

|Build Status| |Code Health| |codecov| |PyPi Version| |GitHub stars|

perfplot extends Python's very own
`timeit <https://docs.python.org/2/library/timeit.html>`__ by testing
snippets with input parameters (e.g., the size of an array) and plotting
the results.

For example, to compare different NumPy array concatenation methods, the
script

.. code:: python

    import numpy
    import perfplot

    perfplot.show(
            setup=lambda n: numpy.random.rand(n),
            kernels=[
                lambda a: numpy.c_[a, a],
                lambda a: numpy.stack([a, a]).T,
                lambda a: numpy.vstack([a, a]).T,
                lambda a: numpy.column_stack([a, a]),
                lambda a: numpy.concatenate([a[:, None], a[:, None]], axis=1)
                ],
            labels=['c_', 'stack', 'vstack', 'column_stack', 'concat'],
            n_range=[2**k for k in range(15)],
            xlabel='len(a)'
            )

produces

.. figure:: https://nschloe.github.io/perfplot/concat.png
   :alt: 

Clearly, ``stack`` and ``vstack`` are the best options for large arrays!

Installation
~~~~~~~~~~~~

Python Package Index
^^^^^^^^^^^^^^^^^^^^

perfplot is `available from the Python Package
Index <https://pypi.python.org/pypi/perfplot/>`__, so simply type

::

    pip install -U perfplot

to install or upgrade.

Manual installation
^^^^^^^^^^^^^^^^^^^

Download perfplot from `GitHub <https://github.com/nschloe/perfplot>`__
and install it with

::

    python setup.py install

Testing
~~~~~~~

To run the perfplot unit tests, check out this repository and type

::

    pytest

Distribution
~~~~~~~~~~~~

To create a new release

1. bump the ``__version__`` number,

2. publish to PyPi and tag on GitHub:

   ::

       $ make publish

License
~~~~~~~

perfplot is published under the `MIT
license <https://en.wikipedia.org/wiki/MIT_License>`__.

.. |Build Status| image:: https://travis-ci.org/nschloe/perfplot.svg?branch=master
   :target: https://travis-ci.org/nschloe/perfplot
.. |Code Health| image:: https://landscape.io/github/nschloe/perfplot/master/landscape.png
   :target: https://landscape.io/github/nschloe/perfplot/master
.. |codecov| image:: https://codecov.io/gh/nschloe/perfplot/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/nschloe/perfplot
.. |PyPi Version| image:: https://img.shields.io/pypi/v/perfplot.svg
   :target: https://pypi.python.org/pypi/perfplot
.. |GitHub stars| image:: https://img.shields.io/github/stars/nschloe/perfplot.svg?style=social&label=Star&maxAge=2592000
   :target: https://github.com/nschloe/perfplot


