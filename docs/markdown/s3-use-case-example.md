***
# S3 Use Case:  Accessing S3 using stslib credentials
***

* Jenkins IAM user used to assume roles
* Require access to roles in other accounts for extended duration (> 1 hour)
* Auto-refresh of credentials, once per hour

```python

    import stslib


    sts_object = stslib.StsCore(profile_name='jenkinsIAMUser')
    token = sts_object.generate_session_token(lifetime=4)          # 4 hours

    role_list = [

        'RoleNameAccount1',
        'RoleNameAccount2',
        'RoleNameAccount3'
    ]

    sts_object.generate_credentials(role_list)
    credentials = sts_object.current_credentials

    print( credentials() )

    {
        'sts-RoleNameAccount1': <stslib.vault.STSingleSet at 0x7fee0ae05c88>,
        'sts-RoleNameAccount2': <stslib.vault.STSingleSet at 0x7fee0ae05f60>,
        'sts-RoleNameAccount3': <stslib.vault.STSingleSet at 0x7fee0ae05fd0>
    }


    # let's start with account 1 role


    session = boto3.Session(
        aws_access_key_id=credentials()['sts-RoleNameAccount1'].access_key,
        aws_secret_access_key=credentials()['sts-RoleNameAccount1'].secret_key,
        aws_session_token=credentials()['sts-RoleNameAccount1'].session
    )

        # Note:  no region_name param required in the session bc s3 global service

    s3_client = session.client('s3')

```

***

( [Back to Code Examples Index](./index-code-examples.md) )

***
