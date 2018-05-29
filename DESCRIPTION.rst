
**stslib** | Library for generation of Temporary STS Credentials
-----------------------------------------------------------------

``stslib`` automates IAM user access key rotation from the cli by allowing ad hoc or
scheduled renewal of your access key credentials via the Amazon API's.

**stslib**:

    * is a safe and reliable way to rotate (renew) access keys to Amazon Web Services as frequently as you wish, with minimal effort and risk.
    * requires only the profile name of your IAM user in your local `awscli configuration <https://docs.aws.amazon.com/cli/latest/reference/>`__

**Features**:

    * access key rotation via the Amazon APIs
    * key rotation includes:

        * creation of new access keys
        * automated installation in the local `awscli configuration <http://docs.aws.amazon.com/cli/latest/userguide/cli-config-files.html>`__
        * deprecated key deletion

    * automated, unattended key rotation
    * rotate keys as frequently as you wish (daily, for example)
