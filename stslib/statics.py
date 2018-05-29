"""
Summary:
    stslib Project-level Defaults and Settings

    NOTE: local defaults for your specific installation are derived from
          settings found in ~/.stslib/config.yml

Module Attributes:
    - user_home (TYPE str):
        $HOME environment variable, present for most Unix and Unix-like POSIX systems
    - config_dirname (TYPE str):
        directory name default for stslib config files (.stslib)
    - config_path (TYPE str):
        default for stslib config files, includes config_dirname (~/.stslib)
    - sts_min (TYPE int):
        min Amazon STS temp credential lifetime (minutes)
    - sts_max (TYPE int):
        max Amazon STS temp credential lifetime (minutes)
    - token_life_default (TYPE int):
        Default valid lifetime for Amazon STS generated session tokens (minutes)
    - credential_life_default (TYPE int):
        Default valid lifetime for Amazon STS generated temp credentails (minutes)
    - awscli_creds (TYPE str):
        Path including filename to the default awscli credentials file
    - awscli_creds_alternate (TYPE str):
        Path including filename to the alternate default awscli credentials file
    - default_awscli (TYPE str):
        valid local location of the default awscli credentials file. Either
        awscli_creds or awscli_creds_alternate
    - default_output (TYPE str):
        default output file written to disk during refactoring operations

"""

import os
import datetime
import inspect
import logging
import yaml
from stslib._version import __version__

logger = logging.getLogger(__version__)
logger.setLevel(logging.INFO)


# --  declarations  ----------------------------------------------------------


def read_local_config(cfg):
    """ Parses local config file for override values

    Args:
        local_file (str):  filename of local config file

    Returns:
        dict of values contained in local config file
    """
    with open(cfg, 'r') as stream:
        try:
            yml_object = yaml.load(stream)
            #print(yml_object)
            return {
                'log_mode': yml_object['LocalConfiguration']['logging']['log_mode'],
                'log_file': yml_object['LocalConfiguration']['logging']['log_dir'] + yml_object['LocalConfiguration']['logging']['log_file'],
                'debug': yml_object['LocalConfiguration']['debug'],
                'profile_user': yml_object['LocalConfiguration']['profile_user'][0]['Default'],
                'credential_format': yml_object['LocalConfiguration']['CredentialFormat'][0]['Default'],
                }
        except yaml.YAMLError as exc:
            print(exc)

# --  project-level DEFAULTS  ------------------------------------------------

try:

    user_home = os.environ['HOME']

except KeyError as e:
    logger.critical(
        '%s: %s variable is required and not found in the environment' %
        (inspect.stack()[0][3], str(e)))
    raise

else:
    # defaults
    config_dirname = '.stslib'                           # config.cfg
    config_path = user_home + '/' + config_dirname
    sts_max = 2160                                        # minutes
    sts_min = 15                                          # minutes
    token_life_default = 60                               # minutes
    credential_life_default = 60                          # 1 hr (STS Default)
    profile_user = 'default'
    sts_profiles_file = 'profiles.json'
    awscli_creds = user_home + '/' + '.aws/credentials'
    awscli_creds_alternate = os.getenv('AWS_SHARED_CREDENTIALS_FILE')
    default_awscli = awscli_creds_alternate or awscli_creds
    credential_format = 'vault'

    # global vars
    config_filename = 'config.yml'
    config_file = config_path + '/' + config_filename
    config_script = 'local_config.py'
    log_dir = user_home + '/' + 'logs'
    log_filename = 'stslib.log'
    log_file = log_dir + '/' + log_filename
    log_mode = 'stream'
    prefix = 'sts'
    prefix_alt = 'gcreds'

try:
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
        os.chmod(log_dir, 0o755)
    if not os.path.exists(config_file):
        logger.info('%s: %s has not been generated. To customize stslib defaults, run the config script (%s)' %
            (inspect.stack()[0][3],config_file, config_script))
        logger.info('\n\t$ python3 %s\n' % config_script)
        local_config = {}
    else:
        # parse local_config file
        local_config = read_local_config(cfg=config_file)

except OSError as e:
    logger.exception('%s: Error when attempting to access or create %s' %
        (inspect.stack()[0][3], str(e)))
    raise


# --  project-level import objects  ------------------------------------------

defaults = {
    'config_path': config_path,
    'sts_max': datetime.timedelta(minutes=int(sts_max)),
    'sts_min': datetime.timedelta(minutes=int(sts_min)),
    'token_life': datetime.timedelta(minutes=int(token_life_default)),
    'credential_life': datetime.timedelta(minutes=int(credential_life_default)),
    'profile_user': local_config.get('profile_user') or profile_user,
    'output_file': sts_profiles_file,
    'awscli_creds': awscli_creds,
    'awscli_creds_alt': awscli_creds_alternate,
    'default_awscli': default_awscli,
    'format': credential_format
}

global_config = {
    '__version__': __version__,
    'config_file': config_file,
    'log_file': log_file,
    'log_mode': local_config.get('log_mode') or log_mode,
    'credential_prefix': prefix,
    'alternate_prefix': prefix_alt
}
