uData-gouvfr
============


.. image:: https://badges.gitter.im/Join%20Chat.svg
    :target: https://gitter.im/etalab/udata-gouvfr
    :alt: Join the chat at https://gitter.im/etalab/udata-gouvfr


uData customizations for Etalab / Data.gouv.fr.

Compatibility
-------------

**udata-gouvfr** requires Python 2.7+ and `uData`_.


Installation
------------

Install `uData`_.

Remain in the same virtual environment (for Python) and use the same version of npm (for JS).

Install **udata-gouvfr**:

.. code-block:: shell

    git clone https://github.com/etalab/udata-gouvfr.git
    pip install -e udata-gouvfr



Modify your local configuration file of **udata** (typically, `udata.cfg`) as following:

.. code-block:: python

    PLUGINS = ['gouvfr']
    THEME = 'gouvfr'



Build the assets:

.. code-block:: shell

    inv assets



You can list available development commands with:

.. code-block:: shell

    inv -l




.. _circleci-url: https://circleci.com/gh/etalab/udata-gouvfr
.. _circleci-badge: https://circleci.com/gh/etalab/udata-gouvfr.svg?style=shield
.. _gitter-badge: https://badges.gitter.im/Join%20Chat.svg
.. _gitter-url: https://gitter.im/etalab/udata-gouvfr
.. _uData: https://github.com/opendatateam/udata

Changelog
=========

1.0.6 (2017-04-18)
------------------

- Fixed numbering in system integrator FAQ (thanks to Bruno Cornec)
  `#174 <https://github.com/etalab/udata-gouvfr/pull/174>`_
- Added a footer link to the SPD page
  `#176 <https://github.com/etalab/udata-gouvfr/pull/176>`_

1.0.5 (2017-04-06)
------------------

- Added a missing translation
- Alphabetical ordering on SPD datasets

1.0.4 (2017-04-05)
------------------

- Introduce SPD page and badge

1.0.3 (2017-02-27)
------------------

- Translations update
- Switch `udata-js` link to `metaclic` `#161 <https://github.com/etalab/udata-gouvfr/pull/161>`_

1.0.2 (2017-02-21)
------------------

- Optimize png images from theme `#159 <https://github.com/etalab/udata-gouvfr/issues/159>`_
- Optimize png images sizes for territory placeholders `#788 <https://github.com/opendatateam/udata/issues/788>`_

1.0.1 (2017-02-20)
------------------

- Ensure missing FAQ sections raises a 404 `#156 <https://github.com/etalab/udata-gouvfr/issues/156>`_
- Provide deep PyPI versions links into the footer `#155 <https://github.com/etalab/udata-gouvfr/pull/155>`_
- Provide proper cache versionning for theme assets `#155 <https://github.com/etalab/udata-gouvfr/pull/155>`_

1.0.0 (2017-02-16)
------------------

- Remove some main menu entries (events, CADA, Etalab)
- Use a new SVG logo
- Apply changes from `uData 1.0.0 <https://pypi.python.org/pypi/udata/1.0.0#changelog>`_

0.9.1 (2017-01-10)
------------------

- First published release



