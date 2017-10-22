# stsAval | Credential Format Overview

* * *

### 2 Credential Formats

**stsAval** supports 2 different output formats when generating temporary credentials:

1. Format 1:  `vault`, **stsAval** Custom Format (DEFAULT).  
2. Format 2:  `boto`, Native format returned by Amazon's boto library

* Either credential format can be selected by passing the `format` class attribute parameter  
when  instantiating the `StsCore` class.

* * *

### Format 1: `vault` Format (DEFAULT)

* Parameter consumption based on attribute specification
* Additional custom parameter:
    * Duration Attribute (datetime)
    * Expiration Attribute (expiration string format)

```python

    >>> sts_object = StsCore(profile_name='BobSmith')
    >>> code = '123466'
    >>> token = sts_object.generate_session_token(mfa_code=code)
    >>> profile_list = ['DynamoDBRole-dev', 'CodeDeployRole-qa', 'S3ReadOnlyRole-prod']
    >>> sts_object.generate_credentials(profile_list)

    >>> credentials = sts_object.current_credentials

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

    ... etc

```

* * *

### Format 2: `boto` | Amazon STS Native Credential Format

* For use in legacy applications
* Applications where translation of STS credentials is not authorized or discouraged

```python

    from stsAval import StsCore

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

```
* * *

( [Back to README](../../README.md) )


* * *
