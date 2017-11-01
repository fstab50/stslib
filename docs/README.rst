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

Important Documents
~~~~~~~~~~~~~~~~~~~

Before going further, you may wish to understand **stsAval** key concepts and use cases:

-  `Frequently Asked Questions (FAQ) <./FAQ.html>`__
-  `Credential Format Overview <./primer/credential-format-overview.html>`__ -- A primer on the dual credential formats supported by **stsAval**
-  `Code Examples <./primer/index-code-examples.html>`__

------------

**Current Release**:

See `v0.3.6 Release Notes <releases/release_v0.3.6.html>`__

**Previous Releases**

-  `v0.2.1 Release Notes <releases/release_v0.2.1.html>`__
-  `v0.1.8 Release Notes <releases/release_v0.1.8.html>`__

------------

Dependencies
~~~~~~~~~~~~

-  Python3 via one of the following:

   -  Python 3.5+
   -  Python 3.6+

-  Installation of Amazon CLI tools (awscli, see Installation section)
-  Linux Operating System, one of the following:

   -  Redhat Enterprise Linux v7.X
   -  Centos 7.X
   -  Ubuntu 14.04, (Ubuntu 16.04 preferred)
   -  Amazon Linux (2017.09+)

**Note**:

    | Any modern Linux distribution should work, but it must have
    | `Python 3.5 + <http://www.python.org>`_ *as a minimum requirement*.

--------------

Contact
~~~~~~~~~~~~~~~~~~~~~~~~

| **Author**: Blake Huber
| **Slack**: [@blake](https://mpcaws.slack.com/team/blake)
| **Repository**: [@blake](blakeca00[AT]gmail.com)

--------------

( `Table Of Contents <./index.html>`__ )

-----------------

|
