===========================
 README
===========================


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

**Current Feature Release**:

See `v0.3.6 Release Notes <releases/release_v0.3.6.html>`__

**Previous Releases**

-  `v0.2.1 Release Notes <releases/release_v0.2.1.html>`__
-  `v0.1.8 Release Notes <releases/release_v0.1.8.html>`__
-  `v0.3.6D Release Notes <releases/release_v0.3.6D.html>`__

------------

License
~~~~~~~~~

**stsAval** is licensed under `General Public License v3 <./license.html>`__

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
