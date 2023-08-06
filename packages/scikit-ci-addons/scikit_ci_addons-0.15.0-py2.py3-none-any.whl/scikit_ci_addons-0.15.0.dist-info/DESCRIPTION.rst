===============================
scikit-ci-addons
===============================

.. image:: https://readthedocs.org/projects/scikit-ci-addons/badge/?version=latest
    :target: http://scikit-ci-addons.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

scikit-ci-addons is a command line tool and a set of scripts useful to help
drive the CI of projects leveraging services like Appveyor, CircleCI, or TravisCI.

Originally developed to help install prerequisites for building Python
extension, it is now useful to support other type of projects.

Build Status
------------

.. table::

  +---------------+------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------+
  |               | Linux                                                                                    | MacOSX                                                                                      | Windows                                                                                                |
  +===============+==========================================================================================+=============================================================================================+========================================================================================================+
  | PyPI          | .. image:: https://circleci.com/gh/scikit-build/scikit-ci-addons.svg?style=shield        | .. image:: https://img.shields.io/travis/scikit-build/scikit-ci-addons.svg?maxAge=2592000   | .. image:: https://ci.appveyor.com/api/projects/status/gr60jc9hkjlqoo4a?svg=true                       |
  |               |     :target: https://circleci.com/gh/scikit-build/scikit-ci-addons                       |     :target: https://travis-ci.org/scikit-build/scikit-ci-addons                            |    :target: https://ci.appveyor.com/project/scikit-build/scikit-ci-addons/branch/master                |
  +---------------+------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------+

Overall Health
--------------

.. image:: https://codecov.io/gh/scikit-build/scikit-ci-addons/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/scikit-build/scikit-ci-addons

Miscellaneous
-------------

* Free software: Apache Software license
* Documentation: http://scikit-ci-addons.readthedocs.org
* Source code: https://github.com/scikit-build/scikit-addons
* Mailing list: https://groups.google.com/forum/#!forum/scikit-build




History
-------

scikit-ci-addons was initially developed in May 2016 by Omar Padron to facilitate
the continuous integration of the scikit-build project.

At that time, it consisted of code directly embedded in the CI script used in
scikit-build project.

Then, in early September 2016, with the desire to setup cross-platform continuous
integration for other project and avoid duplication or maintenance hell, the code
was factored out by Jean-Christophe Fillion-Robin into a set of reusable scripts
available in the scikit-ci project. By simply cloning the repository, it was
possible to more easily enable CI for other projects.

While this was an improvement, this prevented the distribution of standalone
and simple scikit-ci package. To better separate concerns and facilitate
testing and maintenance, in late September 2016, the scripts were moved into
their own project and scikit-ci-addons was born.

Finally, in late October 2016, Jean-Christophe came up with the concept of
scikit-ci-addons command line tool allowing to execute the scripts (or add-ons)
distributed within the scikit-ci-addons package.


