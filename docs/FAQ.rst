###################################
 Frequently Asked Questions
###################################

- **Q**: For long-lived (auto-refreshed) credentials, how do I ensure that I always have the latest valid credentials?
- **Q**: How do I access ``AccessKeyId`` and ``SecretAccessKey`` values when using stslib's default credential format?
- **Q**: How will **stslib** generate credentials if the profile name in my local awscli config does not match my actual IAM user in my AWS Account?

------------

Auto-Refreshed Credentials
^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Q**: For long-lived (auto-refreshed) credentials, how do I ensure that I always have the latest valid credentials?

**A**: There are 2 methods.

    **Method 1** Call ``current_credentials`` method (Preferred):
    Seting your application to monitor the ``current_credentials``
    method will ensure you receive *only* valid credentials (the method returns None
    for expired credentials). You may use this method when generating temporary credentials
    for any length of time; however, it is especially useful when generating long-lived credentials that are
    auto-refreshed because is it prevents application code from "polling" ``stslib`` to see if new
    credentials have been generated.

        -  use ``current_credentials`` method
        -  returns *only* valid credentials
        -  returns None (``{}``) when credentials are expired

.. code:: python

        >>> sts_object = StsCore(profile_name='BobSmith')
        >>> code = '123466'
        >>> token = sts_object.generate_session_token(mfa_code=code)
        >>> profile_list = ['DynamoDBRole-dev', 'CodeDeployRole-qa', 'S3ReadOnlyRole-prod']
        >>> sts_object.generate_credentials(profile_list)

        >>> credentials = sts_object.current_credentials

        >>> credentials()

        {
            'sts-DynamoDBRole-dev': <stslib.vault.STSingleSet at 0x7fee0ae05c88>,
            'sts-CodeDeployRole-qa': <stslib.vault.STSingleSet at 0x7fee0ae05f60>,
            'sts-S3ReadOnlyRole-prod': <stslib.vault.STSingleSet at 0x7fee0ae05fd0>
        }

| **Method 2**: Monitor the ``StsCore`` credentials class attribute
  containing the latest copy
| of credentials:

.. code:: python


        >>> credentials = sts_object.credentials
        >>> print(credentials)

        {
            'sts-DynamoDBRole-dev': <stslib.vault.STSingleSet at 0x7fee0ae05c88>,
            'sts-CodeDeployRole-qa': <stslib.vault.STSingleSet at 0x7fee0ae05f60>,
            'sts-S3ReadOnlyRole-prod': <stslib.vault.STSingleSet at 0x7fee0ae05fd0>
        }

:ref:`Frequently Asked Questions` Index

--------------

Using ``stslib`` Credentials
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Q**: How do I access ``AccessKeyId`` and ``SecretAccessKey`` values when using stslib's default credential format?

**A**: Example use below:

.. code:: python


        >>> print(credentials)
        {
            'sts-DynamoDBRole-dev': <stslib.vault.STSingleSet at 0x7fee0ae05c88>,
            'sts-CodeDeployRole-qa': <stslib.vault.STSingleSet at 0x7fee0ae05f60>,
            'sts-S3ReadOnlyRole-prod': <stslib.vault.STSingleSet at 0x7fee0ae05fd0>
        }

        >>> credentials['sts-DynamoDBRole-dev'].start
        datetime.datetime(2017, 10, 22, 14, 36, 14, 507887, tzinfo=<UTC>)

        >>> credentials['sts-DynamoDBRole-dev'].end
        datetime.datetime(2017, 10, 22, 15, 36, 14, tzinfo=tzutc())

        >>> credentials['sts-DynamoDBRole-dev'].access_key
        'ASIAIDK76BMAQWUO4AOQ'

        >>> credentials['sts-DynamoDBRole-dev'].secret_key
        'LqzseVc4jnjoqKuJM3+Iiobtz0fButHFu7EpNr07'

        >>> credentials['sts-DynamoDBRole-dev'].expiration     # expiration str in isoformat
        '2017-10-22T15:36:14+00:00'

:ref:`Frequently Asked Questions` Index


--------------

Miscellaneous Questions
^^^^^^^^^^^^^^^^^^^^^^^

**Q**: How will **stslib** generate credentials if the profile name in my local awscli
config does not match my actual IAM user in my AWS Account?

**A**: Some basic calls to AWS' sts and iam services do not require MFA even when the
Amazon API is protected with MFA. At instantiation, **stslib** maps profile names
given to assume roles to IAM users in your account to pinpoint the real IAM username to
be used when assuming roles.

:ref:`Frequently Asked Questions` Index

--------------

( `Table Of Contents <./index.html>`__ )

-----------------

|
