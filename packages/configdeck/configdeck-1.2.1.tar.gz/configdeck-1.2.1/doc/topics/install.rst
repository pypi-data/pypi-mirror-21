=========================
How to install configdeck
=========================

This document will get you up and running with configdeck.

Install Python
==============

Being a Python library, configdeck requires Python.

It works with any Python version from 2.6 to 2.7 (due to backwards
incompatibilities in Python 3.0, configdeck does not currently work with
Python 3.0; see :doc:`the configdeck FAQ </faq/install>` for more
information on supported Python versions and the 3.0 transition).

Get Python at http://www.python.org. If you're running Linux or Mac OS X, you
probably already have it installed.


Remove any old versions of configdeck
=====================================

If you are upgrading your installation of configdeck from a previous version,
you will need to uninstall the old configdeck version before installing the
new version.

If you installed configdeck using ``setup.py install``, uninstalling
is as simple as deleting the ``configdeck`` directory from your Python
``site-packages``.

If you installed configdeck from a Python egg, remove the configdeck ``.egg`` file,
and remove the reference to the egg in the file named ``easy-install.pth``.
This file should also be located in your ``site-packages`` directory.

..  _finding-site-packages:

..  admonition:: Where are my ``site-packages`` stored?

    The location of the ``site-packages`` directory depends on the operating
    system, and the location in which Python was installed. To find out your
    system's ``site-packages`` location, execute the following:

    ..  code-block:: bash

        python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()"

    (Note that this should be run from a shell prompt, not a Python interactive
    prompt.)

..  _install-configdeck-code:

Install the configdeck code
===========================

Installation instructions are slightly different depending on whether you're
installing a distribution-specific package, downloading the latest official
release, or fetching the latest development version.

It's easy, no matter which way you choose.

Installing a distribution-specific package
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Check the :doc:`distribution specific notes </misc/distributions>` to see if your
platform/distribution provides official configdeck packages/installers.
Distribution-provided packages will typically allow for automatic installation
of dependencies and easy upgrade paths.

..  _installing-official-release:

Installing an official release
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    1.  Download the latest release from our `download page`_.

    2.  Untar the downloaded file (e.g. ``tar xzvf configdeck-NNN.tar.gz``,
        where ``NNN`` is the version number of the latest release).
        If you're using Windows, you can download the command-line tool
        bsdtar_ to do this, or you can use a GUI-based tool such as 7-zip_.

    3.  Change into the directory created in step 2 (e.g. ``cd configdeck-NNN``).

    4.  If you're using Linux, Mac OS X or some other flavor of Unix, enter
        the command ``sudo python setup.py install`` at the shell prompt.
        If you're using Windows, start up a command shell with administrator
        privileges and run the command ``setup.py install``.

These commands will install configdeck in your Python installation's
``site-packages`` directory.

..  _bsdtar: http://gnuwin32.sourceforge.net/packages/bsdtar.htm
..  _7-zip: http://www.7-zip.org/

..  _installing-development-version:

Installing the development version
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  admonition:: Tracking configdeck development

    If you decide to use the latest development version of configdeck,
    you'll want to pay close attention to the changes made on trunk, until
    we manage to implement a better way of notifying about changes being made.
    This will help you stay on top
    of any new features you might want to use, as well as any changes
    you'll need to make to your code when updating your copy of configdeck.
    (For stable releases, any necessary changes are documented in the
    release notes.)

If you'd like to be able to update your configdeck code occasionally with the
latest bug fixes and improvements, follow these instructions:

1.  Make sure that you have Git_ installed, and that you can run its
    commands from a shell. (Enter ``git --help`` at a shell prompt to test
    this.)

2.  Check out configdeck's code repository like so:

    ..  code-block:: bash

        git clone https://pagure.io/python-configdeck.git configdeck

3.  Next, make sure that the Python interpreter can load configdeck's code. The most
    convenient way to do this is to use setuptools' develop target.
    For example, on a Unix-like system:

    ..  code-block:: bash

        cd configdeck
        python setup.py develop

When you want to update your copy of the configdeck source code, just run the
command ``git pull`` from within the ``configdeck`` directory. When you do
this, Git will automatically download any changes.

..  _`download page`: https://pagure.io/python-configdeck
..  _Git: https://git-scm.com/
..  _`modify Python's search path`: http://docs.python.org/install/index.html#mo
