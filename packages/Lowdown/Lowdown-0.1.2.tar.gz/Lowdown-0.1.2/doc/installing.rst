..
    :copyright: Copyright (c) 2014 ftrack

.. _installing:

**********
Installing
**********

.. highlight:: bash

Installation is simple with `pip <http://www.pip-installer.org/>`_::

    pip install lowdown

Building from source
====================

You can also build manually from the source for more control. First obtain a
copy of the source by either downloading the
`zipball <https://bitbucket.org/ftrack/lowdown/get/master.zip>`_ or
cloning the public repository::

    git clone git@bitbucket.org:ftrack/lowdown.git

Then you can build and install the package into your current Python
site-packages folder::

    python setup.py install

Alternatively, just build locally and manage yourself::

    python setup.py build

Building documentation from source
----------------------------------

To build the documentation from source::

    python setup.py build_sphinx

Then view in your browser::

    file:///path/to/lowdown/build/doc/html/index.html

Dependencies
============

* `Python <http://python.org>`_ >= 2.6, < 3
* `docutils <http://docutils.sourceforge.net/>`_ >= 0.12, < 1',
* `arrow <http://crsmithdev.com/arrow/>`_ >= 0.4.4, < 1'

Additional For building
-----------------------

* `Sphinx <http://sphinx-doc.org/>`_ >= 1.2.3, < 2
* `sphinx_rtd_theme <https://github.com/snide/sphinx_rtd_theme>`_ >= 0.1.6, < 1
