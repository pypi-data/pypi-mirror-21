Quick install guide
===================

Install configdeck
------------------

You've got three easy options to install configdeck:

    * Install a version of configdeck :doc:`provided by your operating system
      distribution </misc/distributions>`. This is the quickest option for those
      who have operating systems that distribute configdeck.

    * :ref:`Install an official release <installing-official-release>`. This
      is the best approach for users who want a stable version number and aren't
      concerned about running a slightly older version of configdeck.

    * :ref:`Install the latest development version
      <installing-development-version>`. This is best for users who want the
      latest-and-greatest features and aren't afraid of running brand-new code.

..  admonition:: Always refer to the documentation that corresponds to the
    version of configdeck you're using!

    If you do either of the first two steps, keep an eye out for parts of the
    documentation marked **new in development version**. That phrase flags
    features that are only available in development versions of configdeck, and
    they likely won't work with an official release.


Verifying
---------

To verify that configdeck can be seen by Python, type ``python`` from your shell.
Then at the Python prompt, try to import configdeck::

    >>> import configdeck
    >>> print configdeck.__version__
    1.0


That's it!
----------

That's it -- you can now :doc:`move onto the quickstart guide </intro/quickstart>`.
