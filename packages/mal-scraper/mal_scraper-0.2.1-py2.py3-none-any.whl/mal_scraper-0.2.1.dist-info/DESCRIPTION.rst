========
Overview
========



 MyAnimeList web scraper is a Python library for gathering data for analysis.


Usage
=====

Use the `online documentation <https://mal-scraper.readthedocs.io/>`_, and just::

    pip install mal-scraper

We follow `Semantic Versioning <http://semver.org/>`_.


Development
===========

Please see the `Contributing <https://mal-scraper.readthedocs.io/en/latest/contributing.html>`_
documentation page for full details, and especially look at the tips section.

After cloning, and creating a virtualenv, install the development dependencies::

    pip install -e .[develop]

To run the all tests, skipping the python interpreters you don't have::

    tox --skip-missing-interpreters

Project Notes:

- Tests will always mock requests to the internet. You can set the environment
  variable :code:`LIVE_RESPONSES=1` to properly test web scraping.
- You can look at coverage results inside :code:`htmlcov/index.html`.

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox


Changelog
=========

0.2.1 (2017-05-01)
-----------------------------------------

* Add Season as an Enum rather than a simple string (backwards-incompatible)
* Fix failing tests due to version number

0.2.0 (2017-05-01)
-----------------------------------------

* Alter anime retrieval API to use exceptions (backwards-incompatible)
* Improve documentation (mainly around the anime API)

0.1.0 (2016-05-15)
-----------------------------------------

* First release on PyPI.


