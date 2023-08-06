=============
PyPI Uploader
=============

.. image:: https://secure.travis-ci.org/ignacysokolowski/pypi-uploader.png
  :target: http://travis-ci.org/ignacysokolowski/pypi-uploader

.. image:: https://coveralls.io/repos/ignacysokolowski/pypi-uploader/badge.png
   :target: https://coveralls.io/r/ignacysokolowski/pypi-uploader

.. image:: https://pypip.in/v/pypi-uploader/badge.png
  :target: https://crate.io/packages/pypi-uploader/

.. image:: https://pypip.in/d/pypi-uploader/badge.png
  :target: https://crate.io/packages/pypi-uploader/

Upload source distributions of your requirements to your PyPI server.


The problem
===========

If you are using a custom PyPI server as a proxy and want to upload some
packages there, it's not easy.  For each package, you need to download its
source and upload it using ``setup.py`` script:

.. code-block:: bash

    # Uploading requests==2.0.0
    $ git clone https://github.com/kennethreitz/requests
    $ cd requests
    $ git checkout v2.0.0
    # Assuming you have 'internal' index-server configured in your '~/.pypirc'.
    $ python setup.py sdist upload -r internal
    # Uploading coverage==3.5
    $ cd ..
    $ git clone https://github.com/nedbat/coveragepy
    $ cd coveragepy
    $ git checkout coverage-3.5
    $ python setup.py sdist upload -r internal

You could also download the packages directly into the PyPI's index directory.

.. code-block:: bash

    $ ssh pypi-mirror.yourdomain.com
    $ pip install requests==2.0.0 coverage==3.5 -d ~/.packages

If there's more than one package, you could use a requirements file.

.. code-block:: bash

    $ scp requirements.txt pypi-mirror.yourdomain.com:.
    $ ssh pypi-mirror.yourdomain.com
    $ pip install -r requirements.txt -d ~/.packages

But it's still too much.  You should be able to do it with one command.
And what if you don't have SSH access to the PyPI server host?


The solution
============

One command for download and upload.


Upload packages by name
-----------------------

.. code-block:: bash

    $ pypiupload packages mock==1.0.1 requests==2.2.1 -i internal


Upload packages from requirements file
--------------------------------------

.. code-block:: bash

    $ pypiupload requirements requirements.txt -i internal


Upload source distribution files
--------------------------------

.. code-block:: bash

    $ pypiupload files packages/mock-1.0.1.tar.gz \
      packages/requests-2.2.1-py2.py3-none-any.whl -i internal


More options
------------

.. code-block:: bash

    $ pypiupload --help
    $ pypiupload <command> --help


Supported PyPI servers
======================

Tested only on `pypiserver <http://pypi.python.org/pypi/pypiserver>`_.


Installation
============

Install from PyPI::

    $ pip install pypi-uploader

Or go to the root directory with **setup.py** script and install it::

    $ python setup.py install


Documentation
=============

Documentation is available at https://pypi-uploader.readthedocs.org


Source
======

Source is available at https://github.com/ignacysokolowski/pypi-uploader


License
=======

PyPI Uploader is licensed under the :ref:`MIT license <license>`.


Changelog
=========

Version 1.1.0
-------------

* Adapt to newer versions of pip: use ``pip download`` instead of
  ``pip install`` for downloading packages, and ``--no-binary :all:`` instead
  of ``--no-use-wheel`` to not use wheel archives.

Version 1.0.0
-------------

* Added ``--no-use-wheel`` option

Version 0.1.0
-------------

First release


Issues and contributing
=======================

Please report any issues on GitHub at
https://github.com/ignacysokolowski/pypi-uploader/issues

Or contribute by submitting a pull request with your changes following these
rules:

* Follow :pep:`8` rules
* Follow :pep:`257` rules
* Follow The Zen of Python
* Test your commits
* Write meaningful commit messages
* Keep the documentation up-to-date

To run tests and build the docs, you have to install additional packages::

    $ python setup.py develop
    $ pip install -r requirements_dev.txt

Running tests::

    $ tox

Building documentation::

    $ cd docs
    $ make html


API Reference
=============

.. toctree::
   :maxdepth: 5

   api/index


==================
Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
