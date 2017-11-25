"""
local_config Module

    processes local config file (yaml) if exists

"""
import os
import yaml
import logging
from stsAval._version import __version__

logger = logging.getLogger(__version__)
logger.setLevel(logging.INFO)


class LocalConfig():
    def __init__(self, local_file=''):
        if os.path.exists(local_file):
            self.read(local_file)
        else:
            logger.info(
                'local config file [%s] not found, creating.' %
                global_config['config_file']
                )
            self.create(local_file)
            self.read(local_file)
        return

    def read(self, cfg):
        """ reads values from local config file """
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



    def update(self):
        """ updates values in local config file """

    def create(cfg):
        """ create new config file """
        with open(cfg, 'w') as f1:
            f1.write(seed_file)
            f1.close()
        return

seed_file = """
# -----------------------------------------------------------------------------
#        stsAval Configuration File Defaults
# -----------------------------------------------------------------------------

LocalConfiguration:
    logging:
        log_mode: 'file'
        log_dir: '~/.stsaval'
        log_file: '/' + 'stsaval.log'

    token_life_default: 60

    credential_life_default: 60

    debug: False

    profile_user:
        - Default: 'default'

    CredentialFormat:
        - Default: 'vault'

    CredentialPrefix:
        - Default: 'sts'
        - omit-prefixes: ['sts', 'gcreds']

"""
