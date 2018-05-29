"""
Summary:
    stslib generates temporary credentials used to assume roles across
    many AWS accounts. It is commonly used for progammatic use cases where
    avoiding a multi-factor auth prompt in a cli environment is desired

Module Attributes:
    logger - logging object

Example Usage:
    see https://bitbucket.org/blakeca00/stslib/overview
"""

import os
import json
from json import JSONDecodeError
import datetime
import inspect
import yaml
import pytz
import boto3
from botocore.exceptions import ClientError, ProfileNotFound
from stslib import logd
from stslib.refactor import parse_awscli
from stslib.vault import STSToken, STSCredentials
from stslib.async import TimeKeeper, convert_time
from stslib.statics import defaults, global_config
from stslib._version import __version__


logger = logd.getLogger(__version__)


class StsCore():
    """
    Class definition, STS credentials library
    """
    def __init__(self, **kwargs):
        """
        Summary: initalization, attribute assignment

        Args:
            :role_file (arg, TYPE: str):
                optional name of a json structured file located stslib config directory
                in users home directory. File contains information about roles for which
                you which to generate temporary credentials
            :output_file (attr, TYPE: str):
                optional non-default filename
            :profile_name (param, TYPE: str):
                user profile configured in local awscli config with permissions to
                assume roles in target aws accounts
            :profile_user (attr, TYPE: str):
                Instance attr for profile_name when passed as a parameter
            :log_mode (attr, TYPE: str):
                Parameter designation for file or stream log output.  If 'file', output
                defaults to filesystem location denoted in statics module in the
                global_config dict.
            :format (attr, TYPE: str):
                format of credentials, either boto (native) or vault (stslib default format)
            :debug (attr, TYPE: bool):
                optional debug flag (DEFAULT = False)
        """
        # validate provided kwargs
        keywords = ('role_file', 'output_file', 'profile_name',
                    'log_mode', 'format', 'debug')
        if self.filter_args(kwargs, *keywords):
            boto_profiles = kwargs.get('role_file', None)
            stslib_profiles = kwargs.get('output_file', defaults['output_file'])
            self.profile_user = kwargs.get('profile_name', defaults['profile_user'])
            self.log_mode = kwargs.get('log_mode', global_config['log_mode'])
            self.format = kwargs.get('format', defaults['format'])
            self.debug_mode = kwargs.get('debug', False)
        else:
            return

        # session attributes and objects
        self.config_dir = defaults['config_path']
        self.refactor(
            input_file=boto_profiles,
            output_file=stslib_profiles,
            force_rewrite=False
            )
        self.session = self._session_init(self.profile_user)

        # static attributes
        self.sts_max = defaults['sts_max']    # minutes, 36 hours
        self.sts_min = defaults['sts_min']    # minutes, 0.25 hours

        # token attributes
        self.token = {}

        # credential attributes
        self.credentials = {}
        self.credential_default = defaults['credential_life']
        self.credential_expiration = ''       # datetime str ("%Y-%m-%d %H:%M:%S")
        self.refresh_credentials = False      # bool, recuring credential gen

        try:
            iam_client = self.session.client('iam')    # client scope separation
            sts_client = self.session.client('sts')    # client scope separation
        except Exception:
            return
        self.users = self.get_valid_users(iam_client)
        self.iam_user = self._map_identity(self.profile_user, sts_client)
        self.mfa_serial = self.get_mfa_info(self.iam_user, iam_client)
        self.thread = None

    def local_config(self):
        """ override defaults in statics with local config values """
        if os.path.exists(global_config['config_file']):
            with open(global_config['config_file'], 'r') as stream:
                try:
                    yml_object = yaml.load(stream)
                except yaml.YAMLError as exc:
                    print(exc)
                else:
                    self.log_mode = yml_object['LocalConfiguration']['log_mode'][0]
        return

    def _map_identity(self, user, client):
        """
        retrieves iam user info for profiles in awscli config

        Args:
            :type user: string, local profile user
            :param user: user from which default boto3 session object created

            :type client: boto3.client
            :param client: the sts client used

        Returns:
            :type iam_user: string
            :param iam_user: AWS iam user mapped to profile user in local config
        """
        try:
            iam_user = client.get_caller_identity()['Arn'].split('/')[1]
            logger.info(
                '%s: profile_name mapped to iam_user: %s' %
                (inspect.stack()[0][3], iam_user)
            )
        except ClientError as e:
            logger.warning(
                '%s: Inadequate User permissions (Code: %s Message: %s)' %
                (inspect.stack()[0][3], e.response['Error']['Code'],
                e.response['Error']['Message']))
            raise str(e)
        return iam_user

    def parse_profiles(self, pre_name, post_name):
        """
        Creates list of account profiles from local configuration file

        Args:
            :type string
            :param pre_name: input file containing iam role credentials in
            non-default location or fname

            :type string
            :param post_name: json file containing role profiles for which stslib will
            generate temporary credentials. This file is generated by stslib and
            will be located in the ~/.stslib directory. Format:

        Returns:
            :type: dictionary
            :param profile_dict: list of aws account profile role names, role arns

        .. code-block:: javascript

            {
                "AliceIAMUser": {
                    "aws_access_key_id": "AKIAIDYCI6Q4469WORVQ",
                    "aws_secret_access_key": "Wf2A0dx1ApMrEdljjkjteBmqqCdPB3Ng3kx/ow",
                    "mfa_serial": "arn:aws:iam::715400231659:mfa/AliceIAMUser"
                },
                "DynamoDBAccessRole": {
                    "role_arn": "arn:aws:iam::357115911622:role/DynamoDBFullAccess",
                    "mfa_serial": "arn:aws:iam::715400231659:mfa/AliceIAMUser",
                    "source_profile": "default"
                },
                "EC2AccessRole": {
                    ...
                }
            }

        """

        profile_file = self.config_dir + '/' + str(post_name)

        try:
            if os.path.exists(profile_file):
                with open(profile_file) as f1:
                    profile_dict = json.load(f1)
            else:
                raise OSError(
                    '%s: Problem parsing local awscli credentials file: %s' %
                    (inspect.stack()[0][3], str(profile_file))
                    )
        except JSONDecodeError as e:
            logger.exception(
                '%s: %s file not properly formed json. Error %s' %
                (inspect.stack()[0][3], profile_file, str(e)))
            raise
        except Exception as e:
            logger.exception(e)
            raise
        return profile_dict

    def get_mfa_info(self, user, client):
        """
        Summary:
            Extracts the mfa_serial arn (soft token) or SerialNumber
            (if hardware token assigned)

        Args:
            :type user: string
            :param user:  iam_user in local awscli profile.  user may be a
                profile name which is used exclusively in the awscli but does
                not represent an actual iam name recorded in the Amazon Web
                Services account.

        Returns:
            TYPE: string
        """
        # query local for mfa info
        if self.profile_user in self.profiles.keys():
            if 'mfa_serial' in self.profiles[self.profile_user].keys():
                mfa_id = self.profiles[self.profile_user]['mfa_serial']
            else:
                mfa_id = ''
        else:
            # query aws for mfa info
            try:
                response = client.list_mfa_devices(UserName=user)
                if response['MFADevices']:
                    mfa_id = response['MFADevices'][0]['SerialNumber']
                else:
                    mfa_id = ''
            except ClientError:
                mfa_id = ''    # no mfa assigned to user
            except Exception as e:
                logger.exception(
                    '%s: Unknown error retrieving mfa device info. Error %s' %
                    (inspect.stack()[0][3], str(e)))
                return str(e)
        return mfa_id

    def generate_session_token(self, **kwargs):
        """
        Summary:
            generates session token for use in gen temp credentials

        Args:
            lifetime (int): token lifetime duration in hours
            mfa_code (str): 6 digit authorization code from a multi-factor (mfa)
            authentication device

        Returns:
            session credentials | TYPE: dict

        .. code-block:: javascript

            {
                'AccessKeyId': 'ASIAI6QV2U3JJAYRHCJQ',
                'StartTime': datetime.datetime(2017, 8, 25, 20, 2, 37, tzinfo=tzutc()),
                'Expiration': datetime.datetime(2017, 8, 25, 20, 5, 37, tzinfo=tzutc()),
                'SecretAccessKey': 'MdjPAkXTHl12k64LSjmgTWMsmnHk4cJfeMHdXMLA',
                'SessionToken': 'FQoDYXdzEDMaDHAaP2wi/+77fNJJryKvAdVZjYKk...zQU='
            }
        """
        # parse parameters
        keywords = ('lifetime', 'mfa_code')
        if self.filter_args(kwargs, *keywords):
            lifetime = kwargs.get('lifetime', 1)
            mfa_code = kwargs.get('mfa_code', '')

        # now, timezone offset aware
        now = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
        token_life = datetime.timedelta(hours=int(lifetime))
        mfa_code = str(mfa_code)
        sts_client = self.session.client('sts')

        try:
            if (self.sts_min < token_life <= self.sts_max):
                if self.mfa_serial:
                    response = sts_client.get_session_token(
                        DurationSeconds=token_life.seconds,
                        SerialNumber=self.mfa_serial,
                        TokenCode=mfa_code
                    )
                else:
                    response = sts_client.get_session_token(
                        DurationSeconds=token_life.seconds
                    )
                response['Credentials']['StartTime'] = now
                # set token and related attributes
                self.token = self._set_session_token(
                    token_object=response['Credentials']
                )
            else:
                logger.warning(
                    '%s: Requested lifetime must be STS service limits (%s - %s hrs)'
                    % (inspect.stack()[0][3], self.sts_min, self.sts_max))
                return {}
        except ClientError as e:
            logger.warning(
                '%s: Exception gen session token with iam user %s (Code: %s Message: %s)' %
                (inspect.stack()[0][3], self.iam_user, e.response['Error']['Code'],
                e.response['Error']['Message'])
                )
            return {'Error': str(e)}
        return self.token

    def generate_credentials(self, accounts, token=None, strict=True):
        """
        Summary:
            generate temporary credentials for profiles

        Args:
            accounts: TYPE: list
                List of account aliases or profile names from the local
                awscli configuration in accounts to assume a role

            strict: TYPE: list
                Determines if strict membership checking is applied to
                aliases found in accounts parameter list. if strict=True
                (Default), then if 1 account profilename given in the accounts
                list, all accounts will be rejected and no temporary credentials
                are generated.  If False, temporary credentials generated
                for all profiles that are valid, only invalid profiles will
                fail to generate credentials

        Returns:
            iam role temporary credentials | TYPE: Dict

        .. code-block:: javascript

            {
                'sts-acme-gen-ra1-prod' : {
                    'AccessKeyId': 'ASIAI6QV2U3JJAYRHCJQ',
                    'Expiration': datetime.datetime(2017, 8, 25, 20, 5, 37, tzinfo=tzutc()),
                    'SecretAccessKey': 'MdjPAkXTHl12k64LSjmgTWMsmnHk4cJfeMHdXMLA',
                    'SessionToken': 'FQoDYXdzEDMaDHAaP2wi/+77fNJJryKvAdVZjYKk...zQU='
                },
                'sts-acme-gen-ra1-dev' : {
                    'AccessKeyId': 'ASIAI6QV2U3 ...',
                }
            }

        """
        # prep, now - tz offset aware
        now = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
        session_token = token or self.token
        prefix = global_config['credential_prefix'] + '-'
        credentials = {}

        try:
            if self._valid_token(session_token):
                # instantiate client
                sts_client = self.session.client(
                    'sts',
                    aws_access_key_id=session_token.access_key,
                    aws_secret_access_key=session_token.secret_key,
                    aws_session_token=session_token.session
                )
                # one-time (non-threaded) creation of credentials
                if self._validate(accounts, strict):
                    for alias in accounts:
                        response = sts_client.assume_role(
                            RoleArn=self.profiles[alias]['role_arn'],
                            DurationSeconds=self.credential_default.seconds,
                            RoleSessionName=prefix + alias
                        )
                        response['Credentials']['StartTime'] = now
                        credentials[prefix + alias] = response['Credentials']
                        if self.format == 'boto':
                            self.credentials = credentials
                        else:
                            self.credentials = STSCredentials(credentials).credentials
                else:
                    return {}    # validation fail
                # branch, auto-refresh or one-time gen of credentials
                if self.refresh_credentials:
                    if self.debug_mode:
                        logger.debug('token_duration = %s min, RefreshCount = %s' %
                            (convert_time(self.token.duration),
                            str(self.token.duration.seconds //3600))
                        )
                    # stop active thread if exists before generating new one
                    self._halt_thread()

                    self.thread = TimeKeeper(
                        roles=accounts,
                        event=self.generate_credentials,
                        RefreshCount=(self.token.duration.seconds // 3600),
                        debug=self.debug_mode
                    )
                    self.thread.start()
                    self.refresh_credentials = False
            else:
                logger.warning('No credentials generated, token is expired')
                return {}    # token expired
        except KeyError as e:
            if not strict:
                logger.info('Strict checking %s, role invalid, skipped' % str(e))
            else:
                raise e
        except ClientError as e:
            logger.critical(
                '%s: Assume role exception in account %s (Code: %s Message: %s)' %
                (inspect.stack()[0][3], alias, e.response['Error']['Code'],
                e.response['Error']['Message']))
            return {}
        return self.credentials

    def current_credentials(self):
        """ returns credentials when refreshed

        Args:
            :type self.credentials: dict
            :param self.credentials: latest credentials generated and stored as class attribute

        Returns:
            Valid credentials | None if expired {}

        """
        if self.credentials:
            if self.calc_lifetime(credentials=self.credentials)[1].seconds > 0:
                return self.credentials
            else:
                logger.info('credentials expired')
        return {}

    def _active_thread(self):
        """
        Summary: determine thread status

        Returns:
            TYPE: Boolean | True = active, False = inactive thread
        """
        if self.thread:
            return self.thread.is_alive()
        return False

    def _halt_thread(self):
        """
        Summary: Stop an active thread

        Returns:
            TYPE: Boolean | True = stopped, False = running
        """
        try:
            if self._active_thread():
                # thread alive
                logger.info('Stopping active thread [%s]' % str(self.thread.name))
                self.thread.halt()
                # msg thread status, alive or dead
                logger.info('Status of thread [%s]: %s' %
                        (str(self.thread.name), str(self.thread.is_alive())
                ))
            else:
                logger.info('thread halt requested, but no active thread')
        except Exception as e:
            logger.critical(
                '%s: Unknown error while attempting to halt thread. Error %s' %
                (inspect.stack()[0][3], str(e)))
            return False
        return True

    def _validate(self, list, check_bit):
        """
        Summary:
            validates parameter list is a subsset of profiles list object
        Args:
            TYPE: list

        Returns:
            TYPE: Boolean
        """

        profile_aliases = []

        for profile in self.profiles.keys():
            profile_aliases.append(profile)

        invalid = set(list) - set(profile_aliases)
        valid = set(list) - set(invalid)

        if set(list).issubset(set(profile_aliases)):
            logger.info('%s: Valid account profile names: %s' %
            (inspect.stack()[0][3], str(list)))
            return True
        elif check_bit:
            # strict checking
            logger.info('%s: Valid account profile names: %s' %
            (inspect.stack()[0][3], str(valid)))
            ex = Exception('%s: Invalid account profiles: %s' %
            (inspect.stack()[0][3], set(invalid)))
            logger.exception(ex)
            return False
        else:
            # relaxed checking
            logger.warning('%s: Valid profile names: %s, Invalid Names: %s' %
            (inspect.stack()[0][3], str(valid)), str(invalid))
            return True

    def _valid_token(self, token=None):
        """
        validate if session token active

        Returns:  TYPE Boolean | True = active, False = expired
        """
        # now, timezone offset aware
        now = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
        if token is None:
            logger.info('cannot generate credentials without a session token')
            return False
        elif now >= token.end:
            logger.warning(
                '%s: token expired on %s' %
                (inspect.stack()[0][3], token['Expiration'].isoformat())
            )
            return False    # expired
        return True

    def _session_init(self, user, region=''):
        """
        Summary:
            creates class-level boto3 session object which is shared across
            StsCore method clients and resources

        Args:
            iam user (required) with adequate iam and sts permissions

        Returns:
            boto3 session object
        """

        try:
            if region:
                session_init = boto3.Session(profile_name=user, region_name=region)
            else:
                session_init = boto3.Session(profile_name=user)
            # FUTURE: support other local creds configs besides awscli; use real iam
            # user to establish session, look up mfa_serial, etc before declaring fail
        except ProfileNotFound:
            return logger.warning(
                '%s: iam user [%s] not found in local awscli configuration.' %
                (inspect.stack()[0][3], user))
            raise
        except ClientError as e:
            logger.critical(
                '%s: Unable to establish session (Code: %s Message: %s)' %
                (inspect.stack()[0][3], e.response['Error']['Code'],
                e.response['Error']['Message'])
                )
            raise
        return session_init

    def _set_session_token(self, token_object):
        """
        Summary:
            update class attributes for newly generated session token

        Args:
            token_object (credentials object) | Amazon STS session token obj

        Returns:  (token, expiration) | TYPE: tuple
            token (datetime obj) | session remaining lifetime (minutes)
            expiration (datetime str) | token lifetime (minutes) datetime string
        """
        drift = datetime.timedelta(minutes=3)
        default_low = self.credential_default - drift
        default_hi = self.credential_default + drift
        # init STSToken obj
        token = STSToken(token_object)

        #token.duration = duration
        if default_low < token.duration < default_hi:
            self.refresh_credentials = False    # enable async cred gen
        elif token.duration >= self.credential_default - drift:
            self.refresh_credentials = True    # enable async cred gen
        logger.debug('refresh_credentials class attribute set to: %s' %
                str(self.refresh_credentials)
                )
        return token

    def _set_credentials(self, c_object):
        """
        Summary:
            update class attributes for newly generated credentials

        Args:
            c_object (credentials object): Amazon STS temporary credentials obj

        Returns:
            tuple (token, expiration)
            credentials (datetime obj) | session remaining lifetime (minutes)
            expiration (datetime str) | remaining time credentials are valid
        """

        try:
            # set class attributes
            expiration = c_object['Expiration'].isoformat()
        except NameError:
            return logger.warning('%s: there is no active session established' %
            inspect.stack()[0][3])
        return c_object, expiration

    def calc_lifetime(self, credentials=None, human_readable=False):
        """ Return remaining time on sts token, sts temporary credentials

        Args:
            :type credentials:  STSCredentials object (if specified)
            :param credentials: generated for which remaining life requested

            :type self.token: STSToken object (if exists)
            :param self.token: latest token generated

        Returns:
            tuple containing TYPE: datetime.timedelta objects (DEFAULT)
            human_readable: returns tuple containing strings

        .. code-block:: javascript

                (
                    token_life_remaining,
                    credential_life_remaining
                )
        """
        try:
            # now, timezone offset aware
            now = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)

            credentials = self.credentials
            keys = []
            for key in credentials:
                keys.append(key)
            if self.format == 'boto':
                credential_expiration = credentials[keys[0]]['Expiration']
            else:
                credential_expiration = credentials[keys[0]].end

            if self.token:
                if self.token.end >= now:
                    token_life_reamining = self.token.end - now
                else:
                    token_life_reamining = datetime.timedelta(minutes=0)
            else:
                token_life_reamining = datetime.timedelta(minutes=0)

            if credentials:
                if credential_expiration >= now:
                    credential_life_remaining = credential_expiration - now
            else:
                credential_life_remaining = datetime.timedelta(minutes=0)

            if human_readable:
                token_life_reamining = convert_time(token_life_reamining)
                credential_life_remaining = convert_time(credential_life_remaining)
        except Exception as e:
            raise
        return (token_life_reamining, credential_life_remaining)

    def get_valid_users(self, client):
        """
        Summary:
            Retrieve list valid iam users from local config

        Arg:
            iam client object

        Returns:
            TYPE list
        """
        users = []
        try:
            users = [x['UserName'] for x in client.list_users()['Users']]
        except ClientError as e:
            logger.critical(
                '%s: User not valid or permissions inadequate (Code: %s Message: %s)' %
                (inspect.stack()[0][3], e.response['Error']['Code'],
                e.response['Error']['Message']))
            raise
        return users

    def filter_args(self, kwarg_dict, *args):
        """
        Summary:
            arg, kwarg validity test

        Args:
            kwarg_dict: kwargs passed in to calling method or func
            args:  valid keywords for the caller

        Returns:
            True if kwargs are valid; else raise exception
        """
        # unpack if iterable passed in args - TBD (here)
        if kwarg_dict is not None:
            keys = [key for key in kwarg_dict]
            unknown_arg = list(filter(lambda x: x not in args, keys))
            if unknown_arg:
                raise KeyError(
                    '%s: unknown parameter(s) provided [%s]' %
                    (inspect.stack()[0][3], str(unknown_arg))
                )
        return True

    def refactor(self, input_file=defaults['default_awscli'],
                      output_file=defaults['output_file'], force_rewrite=True):
        """
        Summary:
            Refactors native awscli credentials file into a useable form.
            Credentials file in the native format used by awscli is refactored
            into a json file located in the stslib configuration directory
            (typically ~/.stslib) in user's home.

            refactor exists as a StsCore class method so that it refactoring
            operations can be initiated on an ad hoc basis whenever credentails
            are refreshed

        Args:
            input_file (str): pathname of awscli credentails file
            output_file (str): name of json formatted output file, post awscli transformation

        Returns:
            TYPE Boolean | Success or Failure
        """
        response = False

        if not force_rewrite and os.path.exists(output_file):
            # local awscli credentials already refactored
            return True
        else:
            # first-time local awscli refactor or force refresh of existing stslib obj profiles
            logger.info('%s: refactoring awscli credentials file' % inspect.stack()[0][3])
            response = parse_awscli(parameter_input=input_file, parameter_output=output_file)
            if response:
                self.profiles = self.parse_profiles(pre_name=input_file, post_name=output_file)
                return True
            return False
