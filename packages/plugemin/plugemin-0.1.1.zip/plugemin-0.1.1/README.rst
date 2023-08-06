********
Plugemin
********

.. image:: https://travis-ci.org/iLoveTux/plugemin.svg?branch=master
    :alt: Travis-CI Build Status (for Linux)
    :target: https://travis-ci.org/iLoveTux/plugemin

.. image:: https://readthedocs.org/projects/plugemin/badge/?version=latest
    :target: http://plugemin.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

plugemin is a simple utility which uses the amazing jinja2 templating engine
and structured data such as XML, JSON or CSV to plug values into templates
many times. Think of a form letter, but endlessly useful. With this you
can render plain text, HTML, XML, JSON or even Python or C. Anything is
possible as long as it is plain text (UTF is supported) in the end.

plugemin was initially designed to template commands which were to be sent over
SSH to target systems.

Getting Started
===============

These instructions will get you a copy of the project up and running
on your local machine for development and testing purposes.

Prerequisites
-------------

You will need the following software installed:

* Python >= 2.7
* jinja2
* lxml

lxml is the only one which needs a compiler to install. If this is an issue,
I would recomend the great
`Anaconda Python Distribution <https://www.continuum.io/downloads>`_
which includes all the prerequisites installed by default.

Installing
----------

You can install the latest stable version with the following command:

.. code:: bash

    $ pip install plugemin

or for the latest development version, you can use the following command:

.. code:: bash

    $ pip install git+https://github.com/ilovetux/plugemin.git

Running the tests
-----------------

In order to run the tests, you will need to clone the repository and kick off
the tests with a single command. All of that can be done with the following
commands:

.. code:: bash

    $ git clone https://github.com/ilovetux/plugemin
    $ cd plugemin
    $ python setup.py nosetests


That's it, the tests should pass, if they don't please open an
`issue <https://github.com/ilovetux/plugemin/issues>`_ and be sure to include:

* The commands you ran to get your results
* The versions of Python, lxml and jinja2 you have installed
* What Operating system
* Any details which would cause your setup to be considered non-standard
  such as running an obscure version of Linux

Basic Usage
-----------

Plugemin will look for templates in a series of locations and take a
structured data format as input. It will render the template with each
piece of data.

*Example*

in C:\\plugemin\\templates\\backup-delete.j2::

    cp {{src}} {{dst}}
    rm {{src}}

in C:\\tmp\\files.csv::

    src,dst
    /var/log/*,/tmp/.
    /usr/var/log/*,/tmp/.
    /var/www/*,/tmp/.

Then you can use the following command::

    C:\> plugemin -t backup-delete.j2 -d C:\plugemin\files.csv
    cp /var/log/* /tmp/.
    rm /var/log/*
    cp /usr/var/log/* /tmp/.
    rm /usr/var/log/*
    cp /var/www/* /tmp/.
    rm /var/www/*

Contributing
============

Please read
`CONTRIBUTING.rst <https://github.com/iLoveTux/plugemin/blob/master/contributing.rst>`_
for details on our code of conduct, and the process for submitting pull
requests to us.

Versioning
==========

We use `SemVer <http://semver.org/>`_ for versioning. For the versions
available, see the
`tags on this repository <https://github.com/ilovetux/plugemin/tags>`_.

Authors
=======

* `iLoveTux <https://github.com/ilovetux>`_

See also the list of
`contributors <https://github.com/iLoveTux/plugemin/blob/master/contributors>`_
who participated in this project.

License
=======

This project is licensed under the GPL Version 3 or later, please see
the `LICENSE <https://github.com/iLoveTux/plugemin/blob/master/LICENSE>`_
file for details

Acknowledgments
===============

* Hat tip to anyone who's code was used (Jinja2, lxml and Python)
* Brian Kearney and James Brennan for the inspiration to build this utility
* Anyone listed in the contributors file
* Everyone who helps us by submitting issues and pull requests
