"""
Summary:
    Module level constants common across stsaval project

Module Attributes:
    user_home (str):
        $HOME environment variable, present in most shells of Unix and
        Unix-like systems
    config_path(str):
        default for all stsaval config files (~/.stsaval)
    default_awscli (str):
        default awscli credentials file used for input
    default_output (str):
        default output file written to disk during refactoring operations

"""

import os
import datetime
import inspect
import logging
from stsAval._version import __version__

# module attributes
E_DEPENDENCY = 1

logger = logging.getLogger(__version__)
logger.setLevel(logging.INFO)


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
    config_dirname = '.stsaval'                           # config.cfg
    config_path = user_home + '/' + config_dirname
    sts_max = 2160                                        # minutes
    sts_min = 15                                          # minutes
    token_life_default = 60                               # minutes
    credential_life_default = 60                          # 1 hr (STS Default)
    profile_user = 'default'
    post_transform_file = 'profiles.json'
    awscli_creds = user_home + '/' + '.aws/credentials'
    awscli_creds_alternate = os.getenv('AWS_SHARED_CREDENTIALS_FILE')
    default_awscli = awscli_creds_alternate or awscli_creds

    # global vars
    config_file = config_path + '/' + 'stsaval.cfg'
    log_dir = user_home + '/' + 'logs'
    log_file = log_dir + '/' + 'stsaval.log'
    log_mode = 'file'
    prefix = 'sts'
    prefix_alt = 'gcreds'

try:
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
        os.chmod(log_dir, 0o755)
    elif os.path.exists(config_file):
        logger.info('%s: %s has not been generated, using default prefix (%s)' %
            (inspect.stack()[0][3],config_file, prefix)
        )

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
    'profile_user': profile_user,
    'output_file': post_transform_file,
    'awscli_creds': awscli_creds,
    'awscli_creds_alt': awscli_creds_alternate,
    'default_awscli': default_awscli
}

global_config = {
    '__version__': __version__,
    'config_file': config_file,
    'log_dir': log_dir,
    'log_file': log_file,
    'log_mode': log_mode,
    'credential_prefix': prefix,
    'alternate_prefix': prefix_alt
}
