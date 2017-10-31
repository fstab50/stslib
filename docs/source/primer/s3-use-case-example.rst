===============================================
 Accessing Amazon S3 using stsAval credentials
===============================================


-  Jenkins IAM user used to assume roles
-  Require access to roles in other accounts for extended duration (> 1
   hour)
-  Auto-refresh of credentials, once per hour

.. code:: python


        import stsAval


        sts_object = stsAval.StsCore(profile_name='jenkinsIAMUser')
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
            'sts-RoleNameAccount1': <stsAval.vault.STSingleSet at 0x7fee0ae05c88>,
            'sts-RoleNameAccount2': <stsAval.vault.STSingleSet at 0x7fee0ae05f60>,
            'sts-RoleNameAccount3': <stsAval.vault.STSingleSet at 0x7fee0ae05fd0>
        }


        # let's start with 1 role in another account
        # Note: no region_name param necessary in session, s3 global service

        session = boto3.Session(
            aws_access_key_id=credentials()['sts-RoleNameAccount1'].access_key,
            aws_secret_access_key=credentials()['sts-RoleNameAccount1'].secret_key,
            aws_session_token=credentials()['sts-RoleNameAccount1'].session
        )

        s3_client = session.client('s3')

        # list all s3 buckets in the account
        buckets = [x['Name'] for x in s3_client.list_buckets()['Buckets']]

--------------

( `Back to Code Examples <./index-code-examples.html>`__ )
