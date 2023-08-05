Unix: |Unix Build Status| Windows: |Windows Build Status|\ Metrics:
|Coverage Status| |Scrutinizer Code Quality|\ Usage: |PyPI Version|

Overview
========

Compares expected environment variables to those set in production.

Setup
=====

Requirements
------------

-  Python 3.6+

Installation
------------

Install env-diff with pip:

.. code:: sh

    $ pip install env-diff

or directly from the source code:

.. code:: sh

    $ git clone https://github.com/jacebrowning/env-diff.git
    $ cd env-diff
    $ python setup.py install

Usage
=====

Generate a sample config file:

.. code:: sh

    $ env-diff --init

Customize this file to match your project:

-  ``sourcefiles``: contain references to environment variables used in
   your project

   -  ``path``: relative path to source file

-  ``environments``: the environments in which your project runs

   -  ``name``: name of the environment
   -  ``command``: command to display currently set environment
      variables

Display the differences between environment variables in your
environments:

.. code:: sh

    $ env-diff > env-diff.md

Open the generated Markdown table in an appropriate viewer.

.. |Unix Build Status| image:: https://img.shields.io/travis/jacebrowning/env-diff/master.svg
   :target: https://travis-ci.org/jacebrowning/env-diff
.. |Windows Build Status| image:: https://img.shields.io/appveyor/ci/jacebrowning/env-diff/master.svg
   :target: https://ci.appveyor.com/project/jacebrowning/env-diff
.. |Coverage Status| image:: https://img.shields.io/coveralls/jacebrowning/env-diff/master.svg
   :target: https://coveralls.io/r/jacebrowning/env-diff
.. |Scrutinizer Code Quality| image:: https://img.shields.io/scrutinizer/g/jacebrowning/env-diff.svg
   :target: https://scrutinizer-ci.com/g/jacebrowning/env-diff/?branch=master
.. |PyPI Version| image:: https://img.shields.io/pypi/v/env-diff.svg
   :target: https://pypi.python.org/pypi/env-diff

Revision History
================

0.1 (2017-03-30)
----------------

-  Initial alpha release.

0.2 (2017-03-30)
----------------

-  Added detection of source variables matching ``export FOO=bar``.
-  Added Markdown report generation.

0.3 (2017-03-30)
----------------

-  Added CSV report generation.


