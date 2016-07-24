rpymostat-common
========================

.. image:: https://pypip.in/v/rpymostat-common/badge.png
   :target: https://crate.io/packages/rpymostat-common

.. image:: https://pypip.in/d/rpymostat-common/badge.png
   :target: https://crate.io/packages/rpymostat-common

.. image:: https://landscape.io/github/jantman/rpymostat-common/master/landscape.svg
   :target: https://landscape.io/github/jantman/rpymostat-common/master
   :alt: Code Health

.. image:: https://secure.travis-ci.org/jantman/rpymostat-common.png?branch=master
   :target: http://travis-ci.org/jantman/rpymostat-common
   :alt: travis-ci for master branch

.. image:: https://codecov.io/github/jantman/rpymostat-common/coverage.svg?branch=master
   :target: https://codecov.io/github/jantman/rpymostat-common?branch=master
   :alt: coverage report for master branch

.. image:: https://badge.waffle.io/jantman/RPyMostat.png?label=ready&title=Ready
   :target: https://waffle.io/jantman/RPyMostat
   :alt: 'Stories in Ready - waffle.io'

.. image:: http://www.repostatus.org/badges/0.1.0/active.svg
   :alt: Project Status: Active - The project has reached a stable, usable state and is being actively developed.
   :target: http://www.repostatus.org/#active

Common libraries shared by packages in the `RPyMostat <https://github.com/jantman/RPyMostat>`_ project.

This package should not need to be installed on its own; it exists solely to package
shared dependencies for other parts of RPyMostat.

Bugs and Feature Requests
-------------------------

Bug reports and feature requests are happily accepted via the `GitHub Issue Tracker <https://github.com/jantman/rpymostat-common/issues>`_. Pull requests are
welcome. Issues that don't have an accompanying pull request will be worked on
as my time and priority allows.

Development
===========

To install for development:

1. Fork the `rpymostat-common <https://github.com/jantman/rpymostat-common>`_ repository on GitHub
2. Create a new branch off of master in your fork.

.. code-block:: bash

    $ git clone git@github.com:YOURNAME/rpymostat-common.git
    $ cd rpymostat-common
    $ virtualenv . && source bin/activate
    $ python setup.py develop

The git clone you're now in will probably be checked out to a specific commit,
so you may want to ``git checkout BRANCHNAME``.

Guidelines
----------

* pep8 compliant with some exceptions (see pytest.ini)
* 100% test coverage with pytest (with valid tests)

Testing
-------

Testing is done via `pytest <http://pytest.org/latest/>`_, driven by `tox <http://tox.testrun.org/>`_.

* testing is as simple as:

  * ``pip install tox``
  * ``tox``

* If you want to see code coverage: ``tox -e cov``

  * this produces two coverage reports - a summary on STDOUT and a full report in the ``htmlcov/`` directory

* If you want to pass additional arguments to pytest, add them to the tox command line after "--". i.e., for verbose pytext output on py27 tests: ``tox -e py27 -- -v``

Release Checklist
-----------------

1. Open an issue for the release; cut a branch off master for that issue.
2. Confirm that there are CHANGES.rst entries for all major changes.
3. Ensure that Travis tests passing in all environments.
4. Ensure that test coverage is no less than the last release (ideally, 100%).
5. Increment the version number in rpymostat-common/version.py and add version and release date to CHANGES.rst, then push to GitHub.
6. Confirm that README.rst renders correctly on GitHub.
7. Upload package to testpypi, confirm that README.rst renders correctly.

   * Make sure your ~/.pypirc file is correct
   * ``python setup.py register -r https://testpypi.python.org/pypi``
   * ``python setup.py sdist upload -r https://testpypi.python.org/pypi``
   * Check that the README renders at https://testpypi.python.org/pypi/rpymostat-common

8. Create a pull request for the release to be merge into master. Upon successful Travis build, merge it.
9. Tag the release in Git, push tag to GitHub:

   * tag the release. for now the message is quite simple: ``git tag -a vX.Y.Z -m 'X.Y.Z released YYYY-MM-DD'``
   * push the tag to GitHub: ``git push origin vX.Y.Z``

11. Upload package to live pypi:

    * ``python setup.py sdist upload``

10. make sure any GH issues fixed in the release were closed.
