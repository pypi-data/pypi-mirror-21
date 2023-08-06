========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |requires|
        | |coveralls| |codecov|
        | |codacy|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/toba/badge/?style=flat
    :target: https://readthedocs.org/projects/toba
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/SmithSamuelM/toba.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/SmithSamuelM/toba

.. |requires| image:: https://requires.io/github/SmithSamuelM/toba/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/SmithSamuelM/toba/requirements/?branch=master

.. |coveralls| image:: https://coveralls.io/repos/SmithSamuelM/toba/badge.svg?branch=master&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/r/SmithSamuelM/toba

.. |codecov| image:: https://codecov.io/github/SmithSamuelM/toba/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/SmithSamuelM/toba

.. |codacy| image:: https://img.shields.io/codacy/REPLACE_WITH_PROJECT_ID.svg
    :target: https://www.codacy.com/app/SmithSamuelM/toba
    :alt: Codacy Code Quality Status

.. |version| image:: https://img.shields.io/pypi/v/toba.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/toba

.. |commits-since| image:: https://img.shields.io/github/commits-since/SmithSamuelM/toba/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/SmithSamuelM/toba/compare/v0.1.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/toba.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/toba

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/toba.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/toba

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/toba.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/toba


.. end-badges

Timeliness Ordered Byzantine Agreement

* Free software: Apache2 license

Installation
============

::

    pip install toba

Documentation
=============

https://toba.readthedocs.io/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
