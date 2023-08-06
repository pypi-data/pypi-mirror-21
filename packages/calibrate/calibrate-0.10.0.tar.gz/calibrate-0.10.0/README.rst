Calibration
===========

.. image:: https://travis-ci.org/ginkgobioworks/calibrate.svg?branch=master
    :target: https://travis-ci.org/ginkgobioworks/calibrate

This is a simple tool that constructs a calibration curve using known x
and y values from standards, and backout the x value for an unknown
based on its measured y signal.

**Features**

-  Given x and y, creates calibration curve and finds linear portion and
   limits of linearity
-  Given y of an unknown, interpolates to find x
-  Computes interpolation error

Development
-----------

Development requires Docker and Make on your host system. Everything else is taken care of inside the
Docker container.

Spin up your container using the provided ``docker-compose.yml`` file and ``Makefile`` by running
``make image``. This creates an image with a correct git configuration for your user, which makes it
easy to release. All of the commands you should need to run are defined the ``Makefile`` as targets.
All of the targets except for ``image``, are meant to be run inside the Docker container, but can be
run from the host machine by having ``-ext`` appended to them. For example, to run tests, you could
either call ``make test`` from a shell inside the container, or ``make test-ext`` from the host.

Dependencies are managed through the `conda <https://conda.io/docs/>`_ tool and defined in
``environment.yml``. All new dependencies must be specified with a version, for a reproducible build
environment.

All pull requests are run through the Travis CI process specified in ``.travis.yml`` and must pass
all tests before being accepted.

Deployment
----------

Deployment of tagged commits happens to PyPI automatically via Travis CI. To bump and deploy a new
version directly, you must have access to write to the master branch. Run ``make bump/[foo]-ext``,
where ``[foo]`` is ``major``, ``minor``, or ``patch``. Then ``git push origin --tags master``. If
you do not have access to the master branch, do the same thing, but in a separate branch, and make
a pull request.
