==================================
 Dual Credential Format Overview
==================================


Authentication Credential Formats
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**stsAval** supports 2 different output formats when generating
temporary credentials:

1. **stsAval** ``vault`` Format (DEFAULT). Enhanced, custom credential format
2. Native ``boto`` Format. Amazon STS temporary credential format returned by the boto3 python SDK

**Important to Remember**:

    | Either credential format can be selected by setting the ``format`` class attribute parameter
    | when instantiating the ``StsCore`` class.
    |
    | You may change the default **stsAval** format in the
    | config file ``~/stsaval/config.yml``

--------------

stsAval `vault` Format (DEFAULT)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  Access values by specifying credential key + object attribute
-  Out-of-the-box default for stsAval library
-  Additional custom parameters:

   -  ``StartTime``: datetime object representing the datetime stamp of credential generation
   -  ``duration`` Attribute (datetime object)
   -  ``expiration`` Attribute (Expiration datetime stamp in string format)

``vault`` **Code Example**:

.. sourcecode:: python

        >>> from stsAval import StsCore

        >>> sts_object = StsCore(profile_name='BobSmith')
        >>> code = '123466'
        >>> token = sts_object.generate_session_token(mfa_code=code)
        >>> profile_list = [

                'DynamoDBRole-dev', 'CodeDeployRole-qa', 'S3ReadOnlyRole-prod'
            ]

                # where profile_list = list of profile names from local awscli config

        >>> credentials = sts_object.generate_credentials(profile_list)

        >>> print(credentials)

    {
        'sts-DynamoDBRole-dev': <stsAval.vault.STSingleSet at 0x7fee0ae05c88>,
        'sts-CodeDeployRole-qa': <stsAval.vault.STSingleSet at 0x7fee0ae05f60>,
        'sts-S3ReadOnlyRole-prod': <stsAval.vault.STSingleSet at 0x7fee0ae05fd0>
    }

        >>> credentials['sts-DynamoDBRole-dev'].start
        datetime.datetime(2017, 10, 22, 14, 36, 14, 507887, tzinfo=<UTC>)

        >>> credentials['sts-DynamoDBRole-dev'].end
        datetime.datetime(2017, 10, 22, 15, 36, 14, tzinfo=tzutc())

        >>> credentials['sts-DynamoDBRole-dev'].access_key
        'ASIAIDK76BMAQWUO4AOQ'

        >>> credentials['sts-DynamoDBRole-dev'].secret_key
        'LqzseVc4jnjoqKuJM3+Iiobtz0fButHFu7EpNr07'

        >>> credentials['sts-DynamoDBRole-dev'].duration
        datetime.timedelta(0, 3600, 251871)

        >>> credentials['sts-DynamoDBRole-dev'].expiration     # expiration str in isoformat
        '2017-10-22T15:36:14+00:00'

        # Identical attributes available for other roles in the credential set

        >>> credentials['sts-CodeDeployRole-qa'].start
        datetime.datetime(2017, 10, 22, 14, 36, 15, 53567, tzinfo=<UTC>)

        >>> credentials['sts-CodeDeployRole-qa'].end
        datetime.datetime(2017, 10, 22, 15, 36, 15, tzinfo=tzutc())

        >>> credentials['sts-CodeDeployRole-qa'].access_key
        'ASIAIDK76BMA573F4ABD'

        >>> credentials['sts-CodeDeployRole-qa'].secret_key
        'LqzseVc4jnjoqKuJM3+Iiobdlkj9335u7Ep023jlk'

        # ... etc

--------------

( `Table of Contents <../index.html>`__ )

--------------

``boto`` Format \| Amazon STS Native Credential Format
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  Legacy applications
-  Applications where translation of STS credentials is not authorized
   or discouraged
-  Enable format when instantiating ``StsCore`` class (example
   below)

``boto`` **Code Example**:

.. sourcecode:: python

        >>> from stsAval import StsCore

        >>> sts_object = StsCore(profile_name='BobSmith', format='boto')
        >>> token = sts_object.generate_session_token()
        >>> profile_list = [

                'DynamoDBRole-dev', 'CodeDeployRole-qa', 'S3ReadOnlyRole-prod'
            ]

                # where profile_list = list of profile names from local awscli config

        >>> credentials = sts_object.generate_credentials(profile_list)

        >>> print(credentials)         # boto format credentials

    {
      'sts-DynamoDBRole-dev': {
          'StartTime': datetime.datetime(2017, 10, 1, 14, 17, 45, 652218, tzinfo=<UTC>)},
          'Expiration': datetime.datetime(2017, 10, 1, 15, 17, 45, tzinfo=tzutc()),
          'AccessKeyId': 'ASIAJRW7F2BAVN4J34LQ',
          'SecretAccessKey': 'P8EjwTUKL4hil4Y7Ouo9OkFzQ1IxGikbhIjMP5uN',
          'SessionToken': 'FQoDYXdzEDMaDCpxZzDdwWGok/ylQiLcAdlrHCkxP+kvQOes3mnQ0r5GXt...'
      },
      'sts-CodeDeployRole-qa': {
          'StartTime': datetime.datetime(2017, 10, 1, 14, 17, 45, 652218, tzinfo=<UTC>)},
          'Expiration': datetime.datetime(2017, 10, 1, 15, 17, 45, tzinfo=tzutc()),
          'AccessKeyId': 'ASIAIOOOKUYFICAPC6TQ',
          'SecretAccessKey': '3Q+N4UMpbmW7OrvY2mfgbjXxr/qt1L4XqmO+Njpq',
          'SessionToken': 'FQoDYXdzEDMaDL/sJkeAF28UsxE/iyLUAbvBrCUoAkP/eqeS...'
      },
      'sts-S3ReadOnlyRole-prod': {
          'StartTime': datetime.datetime(2017, 10, 1, 14, 17, 45, 652218, tzinfo=<UTC>)}}
          'Expiration': datetime.datetime(2017, 10, 1, 15, 17, 46, tzinfo=tzutc()),
          'AccessKeyId': 'ASIAJPRTS4IXPYGPLKZA',
          'SecretAccessKey': 'EMAfJUz5zMNOyjKl7U2IWpJ0GCtWCos0squOE0wz',
          'SessionToken': 'FQoDYXdzEDMaDO0ekTXJi4+IRWV1ESLXAe1ZfOpmGcS9hbIr...'
      }
    }

--------------

( `Table of Contents <../index.html>`__ )

--------------

Session Token Format
^^^^^^^^^^^^^^^^^^^^

-  Custom **stsAval** Format
-  Access values by specifying token attributes
-  Default token format
-  Additional Parameters not present in STS tokens generated by boto:

   -  ``StartTime``: datetime object representing the datetime stamp of
      credential generation
   -  ``boto``: attribute holding the native STS format of the token as
      returned from Amazon STS

**Session Token Example**:

.. sourcecode:: python

        >>> from stsAval import StsCore

        >>> sts_object = StsCore()
        >>> token = sts_object.generate_session_token()
        >>> print(token)
        <stsAval.vault.STSToken at 0x7f05365e3ef0>

        # token attributes

        >>> print(token.start)
        datetime.datetime(2017, 8, 25, 20, 4, 37, tzinfo=tzutc()

        >>> print(token.end)
        datetime.datetime(2017, 8, 25, 21, 4, 36, tzinfo=tzutc())

        >>> print(token.access_key)
        'ASIAI6QV2U3JJAYRHCJQ'

        >>> print(token.secret_key)
        'MdjPAkXTHl12k64LSjmgTWMsmnHk4cJfeMHdXMLA'

        >>> print(token.session)
        'FQoDYXdzEDMaDHAaP2wi/+77fNJJryKvAa20AqGxoQlcRtf8RFLa5Mps9zK9V5SM3Q7+M3h9iNbcxfaZsUnTzFvFwjVZjYKk...zQU='

        >>> print(token.boto)    # native boto generated format

    {
        'AccessKeyId': 'ASIAI6QV2U3JJAYRHCJQ',
        'StartTime': datetime.datetime(2017, 8, 25, 20, 4, 37, tzinfo=tzutc()),
        'Expiration': datetime.datetime(2017, 8, 25, 21, 4, 36, tzinfo=tzutc()),
        'SecretAccessKey': 'MdjPAkXTHl12k64LSjmgTWMsmnHk4cJfeMHdXMLA',
        'SessionToken': 'FQoDYXdzEDMaDHAaP2wi/+77fNJJryKvAa20AqGxoQlcRtf8RFLa5Mps9zK9V5SM3Q7+M3h9iNbcxfa...zQU='
    }

--------------

( `Back <../index.html>`__ )
