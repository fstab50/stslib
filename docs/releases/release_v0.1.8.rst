===============================
 v0.1.8 \| Release Notes
===============================


**Release date**: September 8, 2017

--------------

Features Implemented, v0.1.8
------------------------------

-  **Thread Management**: Thread persistence solved with threading event based wait states

-  **Token & Credential Lifetime**: Method to retrieve both token and credentials life remaining.
   Two forms returned: datatime.timedelta objects for programmatic use or human\_readable format.

--------------

Limitations, v0.1.8
-------------------

Non-Default Credential Files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  Instantiation of stslib objects with non-default credentials
   filename or file location (ie
   outside of default awscli config) currently broken.

--------------

( `Back to README <../README.html>`__ )

--------------

   |
