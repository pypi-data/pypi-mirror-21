.. ppu documentation master file, created by
   sphinx-quickstart on Sat Apr 15 20:37:34 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Portable Python Utilities
=========================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   install
   news

.. highlight:: none

Command line
------------

cmp.py
~~~~~~

Compare two files.

Usage::

    cmp.py file1 file2

remove-old-files.py
~~~~~~~~~~~~~~~~~~~

Remove old files. It's a portable replacement for
`find start_dir -type f -mtime +31 -delete`.

Usage::

    remove-old-files.py [-e] -o days start_dir

Options::

    -e, --empty-dirs
                           remove empty directories
    -o days, --older days
                           remove files older than this number of days;
                           this is a required option

rm.py
~~~~~

Remove files.

Usage::

    rm.py file1 [file2...]

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
