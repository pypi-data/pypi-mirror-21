Tomographer Python Interface
============================

The Python interface to Tomographer allows you to easily perform reliable
quantum tomography in a Python environment.

Documentation is provided `here
<https://tomographer.github.io/tomographer/api-doc/current/html/py/index.html>`_.


Installation
------------

In order to install this Python extension, you need a relatively recent C++ compiler
(supporting C++11), such as `g++` ≥ 4.8 or `llvm/clang` ≥ 3.3.

The easiest way to install `tomographer` is using `pip`::

    pip install numpy pybind11
    pip install tomographer


*NOTE*: ``pip`` cannot (apparently) install build-time requirements, so you have
to install ``numpy`` and ``pybind11`` manually, before installing ``tomographer``.


License
-------

The Tomographer project is licensed under the MIT license, see LICENSE.txt.

Note: This package contains a subset of the
`Boost library <https://boost.org/>`_
(distributed under the `Boost software license <http://www.boost.org/users/license.html>`_)
and the `Eigen3 library <https://eigen.tuxfamily.org/>`_
(distributed under the `MPL license 2.0 <https://www.mozilla.org/en-US/MPL/2.0/>`_).
They are located in the source package directory ``tomographer/include/deps/``.
