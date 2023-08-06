Coop - base for all Nestbox sites
=================================

This is a base to build all Nestbox sites off. This package contains all the
common code shared between sites, with the ideal Nestbox site containing only
model definitions, templates, and front end assets.

Making a release
----------------

Upgrade the version in ``coop/_version.py``.
Coop follows `semver <http://semver.org/>`_ for its versioning scheme.

Make a virtual environment and activate it. You may already have one from last time:

.. code-block:: bash

    $ python3 -m venv venv
    $ source venv/bin/activate

Then, package up and publish the package:

.. code-block:: bash

    $ ./setup.py sdist
    $ publish-python-package dist/coop-X-Y-Z.tar.gz

And you are done!
