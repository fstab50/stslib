# README :  stsAval
* * *

## Purpose ##

**stsAval** (pronounced "py gee-creds" for _generate credentials_) is the python3 library that requests  
temporary credentials from [Amazon Security Token Service (STS)](http://docs.aws.amazon.com/STS/latest/APIReference/Welcome.html) for roles that normally require  
mfa credentials in order to authenticate.  

A primary use case for **stsAval** library is to generate a temporary set of AWS access credentials for  
automation tools running on your local machine.  

**stsAval** manages temporary credentials generates credentials in memory for applications that  
need access to iam roles at AWS.  If temporary credentials are needed for extended periods (> 1 hour),  
**stsAval** will automatically generate renew sts credentials when needed.

See [v0.2.1 Release Notes](./notes/release_v0.2.1.md)

#### Previous Releases ####
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
    $ sudo -H pip3 install stsaval
```

* Setup and Configuration

```bash
    $ cd /home/user/<stsaval directory>/
    $ python3 ...TBD
```

* * *
## Use Cases & Examples ##
* * *

MFA: Multi-Factor Authentication (6 digit code)

#### Default IAM User, Generate one-time use token (MFA)

* Default IAM user in local awscli config
* MFA protected cli access
* STS Token with default lifetime (60 minutes)

```python
    from stsaval import StsCore

    >>> object = StsCore()
    >>> code = '123566'
    >>> token = object.generate_session_token(mfa_code=code)

    >>> print(token)

{
    'AccessKeyId': 'ASIAI6QV2U3JJAYRHCJQ',
    'StartTime': datetime.datetime(2017, 8, 25, 20, 4, 37, tzinfo=tzutc()),
    'Expiration': datetime.datetime(2017, 8, 25, 21, 4, 36, tzinfo=tzutc()),
    'SecretAccessKey': 'MdjPAkXTHl12k64LSjmgTWMsmnHk4cJfeMHdXMLA',
    'SessionToken': 'FQoDYXdzEDMaDHAaP2wi/+77fNJJryKvAdVZjYKk...zQU='
}

```

#### Named IAM user, Generate one-time use token (no MFA)

* IAM user profile in local awscli config
* Token with default lifetime (60 minutes)
* Cli not protected with MFA

```python

    from stsaval import StsCore

    >>> object = StsCore(profile_name='IAM_USER1')
    >>> token = object.generate_session_token()

    >>> print(token)

{
    'AccessKeyId': 'ASIAI6QV2U3JJAYRHCJQ',
    'StartTime': datetime.datetime(2017, 8, 25, 20, 4, 37, tzinfo=tzutc()),
    'Expiration': datetime.datetime(2017, 8, 25, 21, 4, 36, tzinfo=tzutc()),
    'SecretAccessKey': 'MdjPAkXTHl12k64LSjmgTWMsmnHk4cJfeMHdXMLA',
    'SessionToken': 'FQoDYXdzEDMaDHAaP2wi/+77fNJJryKvAdVZjYKk...zQU='
}

```

#### Generation of Credentials

* STS temporary credentials, default lifetime (60 minutes)

```python

    >>> profile_list = [

            'DynamoDBRole-dev', 'CodeDeployRole-qa', 'S3ReadOnlyRole-prod'

        ]

            # where profile_list = list of profile names from local awscli config

    >>> object.generate_credentials(profile_list)

    >>> print(credentials)

{
    'sts-DynamoDBRole-dev': {        
        'StartTime': datetime.datetime(2017, 9, 3, 19, 0, 5, tzinfo=<UTC>)},
        'Expiration': datetime.datetime(2017, 9, 4, 20, 0, 4, tzinfo=tzutc()),
        'AccessKeyId': 'ASIAJRW7F2BAVN4J34LQ',
        'SecretAccessKey': 'P8EjwTUKL4hil4Y7Ouo9OkFzQ1IxGikbhIjMP5uN',
        'SessionToken': 'FQoDYXdzEDMaDCpxZzDdwWGok/ylQiLcAdlrHCkxP+kvQOes3mnQ0r5GXt...'
    },
    'sts-CodeDeployRole-qa': {
        'StartTime': datetime.datetime(2017, 9, 3, 19, 0, 14, tzinfo=<UTC>)},
        'Expiration': datetime.datetime(2017, 9, 4, 20, 0, 13, tzinfo=tzutc()),
        'AccessKeyId': 'ASIAIOOOKUYFICAPC6TQ',
        'SecretAccessKey': '3Q+N4UMpbmW7OrvY2mfgbjXxr/qt1L4XqmO+Njpq',
        'SessionToken': 'FQoDYXdzEDMaDL/sJkeAF28UsxE/iyLUAbvBrCUoAkP/eqeS...'
    },
    'sts-S3ReadOnlyRole-prod': {        
        'StartTime': datetime.datetime(2017, 9, 3, 19, 0, 22, tzinfo=<UTC>)},
        'Expiration': datetime.datetime(2017, 9, 4, 20, 0, 22, tzinfo=tzutc()),
        'AccessKeyId': 'ASIAJPRTS4IXPYGPLKZA',
        'SecretAccessKey': 'EMAfJUz5zMNOyjKl7U2IWpJ0GCtWCos0squOE0wz',
        'SessionToken': 'FQoDYXdzEDMaDO0ekTXJi4+IRWV1ESLXAe1ZfOpmGcS9hbIr...'
    }
}

```

* * *

#### Named IAM user, Generate Extended Use Credentials

* IAM user profile in local awscli config, MFA protected cli
* Token with 5 hour lifetime

```python

    from stsaval import StsCore

    >>> object = StsCore(profile_name='IAM_USER1')
    >>> code = '123566'
    >>> token = object.generate_session_token(lifetime=5, mfa_code=code)

    >>> print(token)

{
    'AccessKeyId': 'ASIAI6QV2U3JJAYRHCJQ',
    'StartTime': datetime.datetime(2017, 9, 21, 20, 4, 37, tzinfo=tzutc()),
    'Expiration': datetime.datetime(2017, 9, 21, 20, 9, 37, tzinfo=tzutc()),
    'SecretAccessKey': 'MdjPAkXTHl12k64LSjmgTWMsmnHk4cJfeMHdXMLA',
    'SessionToken': 'FQoDYXdzEDMaDHAaP2wi/+77fNJJryKvAdVZjYKk...zQU='
}

```

#### Refresh of Credentials

* STS temp credentials will regenerate once per hour, before expiration
* Refresh of credentials is non-blocking (via separate thread)
* Thread management is via event states so threads are terminated as soon as they either  
their associated session token expires or they receive a halt event.
*   No hanging threads. Any threads which are alive when new credentials generated are killed  
before generating a new set.

```python

    >>> profile_list = [

            'DynamoDBRole-dev', 'CodeDeployRole-qa', 'S3ReadOnlyRole-prod'

        ]

            # where profile_list = list of profile names from local awscli config

    >>> credentials_object = object.generate_credentials(profile_list)

```

* **stsAval** returns a method to `credentials_object`.  This method queries StsCore for a class attribute,  
holding the latest credentials generated.
* applications using stsaval need only to access Amazon Web Services' resources by utilising credentials_object  
directly

```python

    >>> print(credentials_object)

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


  >>> print(credentials_object)

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

#### Non-default name or location of credentials file instead of awscli credentials

* Initialization

    < tbd >

* Output

    < tbd >

* * *

#### Use of Non-default IAM Role credentials file located outside of the awscli config

* Initialization

```python

    from stsaval import StsCore

    >>> object = StsCore()
    >>> credentials_file = '~/myAccount/role_credentials'   # awscli credentials file, located in ~/.aws

    >>> object.refactor(credentials_file)

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

see [Frequently Asked Questions](./notes/faq.md)

* * *

## Enhancement Roadmap ##

for a complete list of enhancements logged against the stsaval project, see the [list of stsaval issues](https://bitbucket.org/blakeca00/stsaval/issues?status=new&status=open).
