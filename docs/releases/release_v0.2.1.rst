===============================
 v0.2.1 \| Release Notes
===============================

--------------

**Release date**: September 23, 2017

Features Implemented in v0.2.1
------------------------------

-  **Debug Mode**: Now user configurable

-  **Documentation Updates**: README received extensive updates in this
   release

--------------

Limitations
-----------

Non-Default Credential Files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*Fixed in this version*

-  Instantiation of stsAval objects with non-default credentials filename or file location (ie
   outside of default awscli config) previously broken. Processes role
   profile info correctly when passed to StsCore from a non-standard location outside of ``~/.aws`` when
   contained in a file with a non-standard file name.

--------------

( `Back to README <../README.html>`__ )

--------------

|
