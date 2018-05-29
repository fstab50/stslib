===========================
 Installation
===========================

Dependencies
*************

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
    | `Python 3.5 + <http://www.python.org>`__ *as a minimum requirement*.

--------------


**Linux Distribution**

Choose your operating system for correct installation instructions:

   - :ref:`redhat`
   - :ref:`ubuntu`
   - :ref:`amazonlinux`

**Note**:

    | Any modern Linux distribution should work, but it must have
    | `Python 3.5 + <http://www.python.org>`_ *as a minimum requirement*.

------------

.. _redhat:

Redhat Enterprise Linux v7.X / Centos 7.X
******************************************

-  Install Python3 Package Manager

.. code:: bash

        $ sudo yum install python3-pip

-  Install `awscli <https://github.com/aws/aws-cli/>`__

   Detailed instructions can be found in the README located at:
   https://github.com/aws/aws-cli/

   The easiest method, provided your platform supports it, is via
   `pip <http://www.pip-installer.org/en/latest>`__.

.. code:: bash

        $ sudo pip3 install awscli

-  If you have the aws-cli installed and want to upgrade to the latest
   version you can run:

.. code:: bash

        $ sudo pip3 install --upgrade awscli

-  Installation via pip3 (python3 packages via pip package manager)

.. code:: bash

        $ sudo -H pip3 install stslib

-  Setup and Configuration

.. code:: bash

        $ cd /home/user/<stslib directory>/
        # $  ...TBD


------------------

.. _ubuntu:

Ubuntu v16.04+ / Ubuntu-based Distros
**************************************

-  Install Python3 Package Manager

.. code:: bash

        $ sudo apt-get install python3-pip

-  Install `awscli <https://github.com/aws/aws-cli/>`__

   Detailed instructions can be found in the README located at:
   https://github.com/aws/aws-cli/

   The easiest method, provided your platform supports it, is via
   `pip <http://www.pip-installer.org/en/latest>`__.

.. code:: bash

        $ sudo pip3 install awscli

-  If you have the aws-cli installed and want to upgrade to the latest
   version you can run:

.. code:: bash

        $ sudo pip3 install --upgrade awscli

-  Installation via pip3 (python3 packages via pip package manager)

.. code:: bash

        $ sudo -H pip3 install stslib

-  Setup and Configuration

.. code:: bash

        $ cd /home/user/<stslib directory>/
        # $  ...TBD


------------------

.. _amazonlinux:

Amazon Linux v2017.09 +
***********************

-  Install Python3 Package Manager

.. code:: bash

        $ sudo yum install python36-pip

.. code:: bash

        $ sudo -H pip3 install stslib

-  Setup and Configuration

.. code:: bash

        $ cd /home/user/<stslib directory>/
        $ python3 ...TBD



--------------

( `Table Of Contents <./index.html>`__ )

-----------------

|
