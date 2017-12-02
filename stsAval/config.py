"""
Summary:
    local_config Module, creates local config file (yaml) to override default
    values set in statics module

Module Attributes:
    - config_file (TYPE str):
        Name of local config file, usually found in ~/.stsaval dir
    - logger (TYPE logging obj):
        system logger, output set by log_mode project-level attribute
    - config_seed (TYPE str):
        yaml config file template used to seed local config file if none exists
"""
import os
import yaml
import logging
from stsAval.statics import global_config['config_file']
from stsAval._version import __version__


logger = logging.getLogger(__version__)
logger.setLevel(logging.INFO)



class UpdateConfig():
    def __init__(self, local_file=''):
        if os.path.exists(local_file):
            self.update(local_file)
        else:
            logger.info(
                'local config file [%s] not found, creating.' % config_file)
            self.create(local_file)
        return

    def update(self):
        """ updates values in local config file """

    def create(cfg):
        """ create new config file """
        with open(cfg, 'w') as f1:
            f1.write(config_seed)
            f1.close()
        return


class ReadConfig():
    def __init__(self, local_file=''):
        if os.path.exists(local_file):
            self.read(local_file)
        else:
            logger.info('local config file [%s] not found' % config_file)
            return {}

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


if __name__ == '__main__':
    UpdateConfig(local_file=global_config['config_file'])
