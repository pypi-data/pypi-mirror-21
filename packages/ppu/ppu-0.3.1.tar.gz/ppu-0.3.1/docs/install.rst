Installation using pip
======================

System-wide
-----------

::

    sudo pip install --find-links=http://phdru.name/Software/Python/ --no-index --install-option='-O2' ppu

User mode
---------

::

    pip install --find-links=http://phdru.name/Software/Python/ --no-index --install-option='-O2' --user ppu

For Python 2.6 the command is easy_install.

Installation from sources
=========================

To install the library from sources system-wide run run the following
command:

::

    sudo python setup.py install -O2

If you don't want to install it system-wide you can install it in your
home directory; run run the following command:

::

    python setup.py install -O2 --user

Option '--user' installs scripts into $HOME/.local/bin;
add the directory to your $PATH or move the script to a directory in your
$PATH.
