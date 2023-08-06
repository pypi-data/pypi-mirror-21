Tiny Changelog
==============
.. image:: https://img.shields.io/pypi/v/tiny-changelog.svg
    :target: https://pypi.python.org/pypi/tiny-changelog


Yet another approach to generate simple and slim CHANGELOG file.

Install
-------

.. code-block:: bash

    pip install tiny-changelog

Usage
-----

.. code-block:: bash

    usage: tiny-changelog [-h] [-t TOKEN] -p PROJECT [-s START_DATE] [-o OUTPUT]
                          [--with-unreleased]

    Generate CHANGELOG file.

    optional arguments:
      -h, --help            show this help message and exit
      -t TOKEN, --token TOKEN
                            Github token
      -p PROJECT, --project PROJECT
                            Github project (<owner>/<repo>)
      -s START_DATE, --start-date START_DATE
                            List entries starting as early as YYYY-MM-DD
      -o OUTPUT, --output OUTPUT
                            Output file, defaults to CHANGELOG.md
      --with-unreleased     Include unreleased merged pull requests
