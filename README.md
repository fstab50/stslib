***
# README :  stsAval
***

## Purpose ##

**stsAval** (pronounced "s-t-s aay-val") -- Spanish for "sts _trustee_".

**stsAval** is a python3 library that requests and manages temporary credentials from [Amazon's Security Token Service (STS)](http://docs.aws.amazon.com/STS/latest/APIReference/Welcome.html) on your behalf.  
stsAval generates temporary credentials against roles that reside in any number of AWS accounts.

A primary use case for the **stsAval** library is generation of temporary access credentials for automation tools  
which need to authenticate to Amazon Web Services.  Such automation tooling may be running within AWS; however, commonly  
are running in environments external to AWS such as a local machine.

**stsAval** manages temporary credentials generates credentials in memory for applications that  
need access to iam roles at AWS.  If temporary credentials are needed for extended periods (> 1 hour),  
**stsAval** will automatically renew sts credentials before expiration.

### Important Documents
Before going further, you may wish to understand **stsAval** key concepts and use cases:

* [Frequently Asked Questions (FAQ)](./FAQ.md)
* [Credential Format Overview](./docs/markdown/credential-format-overview.md) -- A primer on the dual credential formats supported by **stsAval**
* [Code Examples](./docs/markdown/index-code-examples.md)

* * *

## Releases

See [v0.3.6 Release Notes](./notes/release_v0.3.6.md)

### Previous Releases ###

* [v0.2.1 Release Notes](./notes/release_v0.2.1.md)
* [v0.1.8 Release Notes](./notes/release_v0.1.8.md)

* * *

## Deployment Owner/ Author ##

Blake Huber  
Slack: [@blake](https://mpcaws.slack.com/team/blake)  
BitBucket: [@blake](blakeca00[AT]gmail.com)

* * *

## Dependencies ##

- Python3 via one of the following:
    - Python 3.5.X+
    - Python 3.6.X+
- Installation of Amazon CLI tools (awscli, see Installation section)
- Linux Operating System, one of the following:
    - Redhat Enterprise Linux v7.X (preferred)
    - Ubuntu 14.04, (Ubuntu 16.04 preferred)
    - Amazon Linux (2017.03+ )

* * *

## Installation - Redhat / Ubuntu ##

* Install [awscli](https://github.com/aws/aws-cli/)

    Detailed instructions can be found in the README located at:
    https://github.com/aws/aws-cli/

    The easiest method, provided your platform supports it, is via [pip](http://www.pip-installer.org/en/latest).

```bash
    $ sudo pip install awscli
```

* If you have the aws-cli installed and want to upgrade to the latest version you can run:

```bash
    $ sudo pip install --upgrade awscli
```

* Installation via pip

```bash
    $ sudo -H pip3 install stsAval
```

* Setup and Configuration

```bash
    $ cd /home/user/<stsAval directory>/
    $ python3 ...TBD
```

* * *
# Use Cases & Examples #
* * *

### Generate Session Token (default IAM User)

* `Default` profile in local awscli config. Default user has permissions to assume roles for which **stsAval**  
will generate credentials
* Token with default lifetime (60 minutes)
* Cli _not_ protected with MFA (Multi-Factor Authentication, 6 digit code)

```python

    from stsAval import StsCore

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

```

### Generate Session Token (named IAM User)

* Named IAM user profile in local awscli config. User has permissions to assume roles for which **stsAval**  
will generate credentials
* MFA protected cli access configuration
* STS Token with default lifetime (60 minutes)

```python

    from stsAval import StsCore

    >>> sts_object = StsCore(profile_name='BobSmith')
    >>> code = '123456'
    >>> token = sts_object.generate_session_token(mfa_code=code)

    >>> print(token.boto)

{
    'AccessKeyId': 'ASIAI6QV2U3JJAYRHCJQ',
    'StartTime': datetime.datetime(2017, 8, 25, 20, 4, 37, tzinfo=tzutc()),
    'Expiration': datetime.datetime(2017, 8, 25, 21, 4, 36, tzinfo=tzutc()),
    'SecretAccessKey': 'MdjPAkXTHl12k64LSjmgTWMsmnHk4cJfeMHdXMLA',
    'SessionToken': 'FQoDYXdzEDMaDHAaP2wi/+77fNJJryKvAdVZjYKk...zQU='
}

```

* * *

### Generate Credentials (1 hour lifetime)

* generate STS temporary credentials, default lifetime (60 minutes)
* Credential format set to 'vault' (default stsAval format)
* **stsAval** supports 2 credential formats.  See the [Credential Format Overview](./docs/markdown/credential-format-overview.md).  

```python

    >>> sts_object = StsCore(profile_name='BobSmith')
    >>> token = sts_object.generate_session_token()
    >>> profile_list = [
            'DynamoDBRole-dev', 'CodeDeployRole-qa', 'S3ReadOnlyRole-prod'
        ]

            # where profile_list = list of profile names from local awscli config

    >>> sts_object.generate_credentials(profile_list)

    >>> print(credentials)     

{
    'sts-DynamoDBRole-dev': <stsAval.vault.STSingleSet at 0x7fee0ae05c88>,
    'sts-CodeDeployRole-qa': <stsAval.vault.STSingleSet at 0x7fee0ae05f60>,
    'sts-S3ReadOnlyRole-prod': <stsAval.vault.STSingleSet at 0x7fee0ae05fd0>
}

```

* * *

### Generate Extended Use Credentials (Multi-hour, Auto-refresh)

* Named IAM user profile in local awscli config. User has permissions to assume roles for which stsAval  
will generate credentials
* MFA protected cli configuration
* Credential format set to 'boto' (native Amazon STS format)
* Credentials auto-refreshed for total 5 hour valid lifetime without MFA auth

```python

    from stsAval import StsCore

    >>> sts_object = StsCore(profile_name='BobSmith', format='boto')     # boto format credentials
    >>> code = '123456'
    >>> token = sts_object.generate_session_token(lifetime=5, mfa_code=code)  
    >>> profile_list = [
            'DynamoDBRole-dev', 'CodeDeployRole-qa', 'S3ReadOnlyRole-prod'
        ]

            # where profile_list = list of profile names from local awscli config

    >>> sts_object.generate_credentials(profile_list)
    >>> credentials = sts_object.current_credentials

```

### Auto-Refresh of Credentials

* **stsAval** will automatically generate new temporary credentials once per hour, prior to expiration
* Refresh of credentials is non-blocking (via threading)
* Thread management is via event states; threads are terminated as soon as their associated  
session token expires or they receive a halt event.
* No hanging threads. Any live threads when new credentials generated are safely terminated  
before generating a new set.

```python

    >>> print(credentials())        

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

# stdout log stream
/stsaval/core.py - 0.2.0 - [INFO]: _validate: Valid account profile names: ['DynamoDBRole-dev', 'CodeDeployRole-qa', 'S3ReadOnlyRole-prod']
/stsaval/async.py - 0.2.0 - [INFO]: executing event: <bound method StsCore.generate_credentials of <stsaval.core.StsCore object at 0x7f91c9df02e8>>
/stsaval/async.py - 0.2.0 - [INFO]: thread identifier: Thread-150
/stsaval/async.py - 0.2.0 - [INFO]: thread Alive status is: True
/stsaval/async.py - 0.2.0 - [INFO]: completed 1 out of 5 total executions
/stsaval/async.py - 0.2.0 - [INFO]: remaining in cycle: 4 hours, 59 minutes


  >>> print(credentials())

{
  'sts-DynamoDBRole-dev': {        
      'StartTime': datetime.datetime(2017, 10, 1, 15, 17, 45, 652218, tzinfo=<UTC>)},
      'Expiration': datetime.datetime(2017, 10, 1, 16, 17, 45, tzinfo=tzutc()),
      'AccessKeyId': 'ASIAJRW7F2BAVN4J34LQ',
      'SecretAccessKey': 'P8EjwTUKL4hil4Y7Ouo9OkFzQ1IxGikbhIjMP5uN',
      'SessionToken': 'FQoDYXdzEDMaDCpxZzDdwWGok/ylQiLcAdlrHCkxP+kvQOes3mnQ0r5GXt...'
  },
  'sts-CodeDeployRole-qa': {
      'StartTime': datetime.datetime(2017, 10, 1, 15, 17, 45, 652218, tzinfo=<UTC>)},
      'Expiration': datetime.datetime(2017, 10, 1, 16, 17, 45, tzinfo=tzutc()),
      'AccessKeyId': 'ASIAIOOOKUYFICAPC6TQ',
      'SecretAccessKey': '3Q+N4UMpbmW7OrvY2mfgbjXxr/qt1L4XqmO+Njpq',
      'SessionToken': 'FQoDYXdzEDMaDL/sJkeAF28UsxE/iyLUAbvBrCUoAkP/eqeS...'
  },
  'sts-S3ReadOnlyRole-prod': {        
      'StartTime': datetime.datetime(2017, 10, 1, 15, 17, 45, 652218, tzinfo=<UTC>)}}
      'Expiration': datetime.datetime(2017, 10, 1, 16, 17, 46, tzinfo=tzutc()),
      'AccessKeyId': 'ASIAJPRTS4IXPYGPLKZA',
      'SecretAccessKey': 'EMAfJUz5zMNOyjKl7U2IWpJ0GCtWCos0squOE0wz',
      'SessionToken': 'FQoDYXdzEDMaDO0ekTXJi4+IRWV1ESLXAe1ZfOpmGcS9hbIr...'
  }
}

# stdout log stream
/stsaval/core.py - 0.2.0 - [INFO]: _validate: Valid account profile names: ['DynamoDBRole-dev', 'CodeDeployRole-qa', 'S3ReadOnlyRole-prod']
/stsaval/async.py - 0.2.0 - [INFO]: thread identifier: Thread-150
/stsaval/async.py - 0.2.0 - [INFO]: thread Alive status is: True
/stsaval/async.py - 0.2.0 - [INFO]: completed 2 out of 5 total executions
/stsaval/async.py - 0.2.0 - [INFO]: remaining in cycle: 3 hours, 59 minutes

```

* * *

### Non-default IAM Role credentials filename or location

**Use-Case**: When you wish to use role credentials file not currently part of the awscli,  
you can provide a custom location to stsAval as a parameter

* Initialization

```python

    import stsAval

    >>> sts_object = stsAval.StsCore()
    >>> credentials_file = '~/myAccount/role_credentials'   # awscli credentials file, located in ~/.aws

    >>> sts_object.refactor(credentials_file)
    >>> sts_object.profiles
```

* Output

```json

{
    "acme-db-dev": {
        "role_arn": "arn:aws:iam::236600111358:role/AcmeDEV",
        "mfa_serial": "arn:aws:iam::3788881165911:mfa/BillCaster",
        "source_profile": "william-caster"
    },
    "acme-apps-dev": {
        "role_arn": "arn:aws:iam::123660943358:role/AcmeDEV",
        "mfa_serial": "arn:aws:iam::3788881165911:mfa/BillCaster",
        "source_profile": "william-caster"
    },
    "acme-apps-qa": {
        "role_arn": "arn:aws:iam::430864833800:role/AcmeAdmin",
        "mfa_serial": "arn:aws:iam::3788881165911:mfa/BillCaster",
        "source_profile": "william-caster"
    },
    "acme-prod08": {
        "role_arn": "arn:aws:iam::798623437252:role/EC2RORole",
        "mfa_serial": "arn:aws:iam::3788881165911:mfa/BillCaster",
        "source_profile": "william-caster"
    },
    "acme-prod09": {
        "role_arn": "arn:aws:iam::123660943358:role/S3Role",
        "mfa_serial": "arn:aws:iam::3788881165911:mfa/BillCaster",
        "source_profile": "william-caster"
    }
}

```

* * *

## FAQ ##

see [Frequently Asked Questions](./FAQ.md)

* * *

## Enhancement Roadmap ##

for a complete list of enhancements logged against the stsAval project, see the [list of stsAval issues](https://bitbucket.org/blakeca00/stsaval/issues?status=new&status=open).
