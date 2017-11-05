===========================
 README
===========================


.. image:: https://img.shields.io/badge/release-v0.3.7-blue.svg

.. image:: https://img.shields.io/jenkins/s/https/jenkins.qa.ubuntu.com/view/Precise/view/All%20Precise/job/precise-desktop-amd64_default.svg

.. image:: https://img.shields.io/readthedocs/pip.svg

.. image::  https://img.shields.io/badge/python-3.5%2C%203.6-blue.svg

.. image:: https://img.shields.io/badge/dependencies-boto3%2C%20awscli%2C%20pytz-yellow.svg

.. image:: https://img.shields.io/badge/License-GPL%20v3-blue.svg

.. image:: https://img.shields.io/badge/platform-linux--64%20%7C%20os--64-lightgrey.svg



Purpose
~~~~~~~

    **stsAval** (pronounced *s-t-s ayy-val*), is a python3 library that requests and manages temporary credentials from
    `Amazon's Security Token Service (STS) <http://docs.aws.amazon.com/STS/latest/APIReference/Welcome.html>`__ on your behalf. The library generates
    temporary credentials against roles that reside in any number of AWS accounts.

    A primary use case for the **stsAval** library is generation of temporary access credentials for
    automation tools which need to authenticate to Amazon Web Services. Such automation tooling may
    be running within AWS; however, commonly are running in environments external to AWS such as a
    local machine.

    **stsAval** manages temporary credentials generates credentials in memory for applications that
    need access to iam roles at AWS. If temporary credentials are needed for extended periods
    (> 1 hour), **stsAval** will automatically renew sts credentials before expiration.

------------

Documentation
~~~~~~~~~~~~~~~

Complete Documentation is available at `http://stsaval.readthedocs.io <http://stsaval.readthedocs.io>`__.

Getting Started
****************

Before starting, read the following to understand **stsAval** key concepts and use cases:

-  `Frequently Asked Questions (FAQ) <./FAQ.html>`__
-  `Credential Format Overview <./primer/credential-format-overview.html>`__ -- A primer on the dual credential formats supported by **stsAval**
-  `Code Examples <./primer/index-code-examples.html>`__

------------

**Current Release**:

See `v0.3.7 Release Notes <releases/release_v0.3.7.html>`__

**Previous Releases**

-  `v0.2.1 Release Notes <releases/release_v0.2.1.html>`__
-  `v0.1.8 Release Notes <releases/release_v0.1.8.html>`__
-  `v0.3.6 Release Notes <releases/release_v0.3.6.html>`__

------------

Use
~~~~~~~~~

.. note::

    | **stsAval** is available via pip in the official `python registry <https://pypi.python.org/pypi>`__
    | and is licensed under the `General Public License v3 <./license.html>`__

------------

Contact
~~~~~~~~~~~~

| **Author**: Blake Huber
| **Slack**: [@blake](https://mpcaws.slack.com/team/blake)
| **Repository**: [@blake](blakeca00[AT]gmail.com)

--------------

( `Table Of Contents <./index.html>`__ )

-----------------

|
