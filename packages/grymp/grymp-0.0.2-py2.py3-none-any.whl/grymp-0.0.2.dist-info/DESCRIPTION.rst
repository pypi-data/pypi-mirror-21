grymp
=====

.. image:: https://img.shields.io/pypi/status/grymp.svg
   :target: https://pypi.python.org/pypi/grymp
.. image:: https://img.shields.io/pypi/v/grymp.svg
   :target: https://pypi.python.org/pypi/grymp
.. image:: https://img.shields.io/pypi/pyversions/grymp.svg
   :target: https://pypi.python.org/pypi/grymp
.. image:: https://travis-ci.org/gebn/grymp.svg?branch=master
   :target: https://travis-ci.org/gebn/grymp
.. image:: https://coveralls.io/repos/github/gebn/grymp/badge.svg?branch=master
   :target: https://coveralls.io/github/gebn/grymp?branch=master
.. image:: https://landscape.io/github/gebn/grymp/master/landscape.svg?style=flat
   :target: https://landscape.io/github/gebn/grymp/master

Automate the processing of Grym/vonRicht releases. Please note: this module does *not* download anything; it only automates renaming and moving around existing files.

Installation
------------

::

    $ pip install grymp

Examples
--------

Process a release called *Release Name* located at ``~/Release.Name-Grym``. The feature will be placed in ``/tmp/features``, and the extras in ``/tmp/extras``:

::

    $ grymp -f /tmp/features -e /tmp/extras ~/Release.Name-Grym "Release Name"

To only process the feature *or* extras, omit ``-f`` (and the path) or ``-e`` (and the path) respectively.

Usage
-----

::

    $ grymp -h
    usage: grymp [-h] [-V] [-v] [-i] [-o] [-k] [-f FEATURE] [-e EXTRAS] base name

    Automate the processing of Grym/vonRicht releases

    positional arguments:
      base                  the root directory of the release, containing the
                            feature
      name                  the name of the feature

    optional arguments:
      -h, --help            show this help message and exit
      -V, --version         show program's version number and exit
      -v, --verbosity       increase output verbosity
      -i, --interactive     prompt before each operation affecting the filesystem
      -o, --overwrite       overwrite files without asking
      -k, --keep            keep original files; only has an effect if they were
                            copied because the destination was on a different
                            filesystem
      -f FEATURE, --feature FEATURE
                            marshal the feature into this directory (it must
                            exist)
      -e EXTRAS, --extras EXTRAS
                            marshal the extras into a new subdirectory within this
                            directory, named after the feature


