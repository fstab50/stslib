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
from stsAval.statics import global_config
from stsAval.colors import Colors
from stsAval.seed import config_seed
from stsAval._version import __version__


logger = logging.getLogger(__version__)
logger.setLevel(logging.INFO)


config_file = global_config['config_file']


class UpdateConfig():
    def __init__(self, local_file):
        if os.path.exists(local_file):
            self.cfg_file=local_file
            self.update(local_file)
        else:
            logger.info(
                'local config file [%s] not found, creating.' % config_file)
            self.create(local_file)
        return

    def update(self, cfg):
        """ updates values in local config file """
        self.print_header('update_header')
        response = input('Ready to begin? ')
        if response:
            log_mode = input(
                'Log output:  Do to log messages to stdout, or to a file? [stdout] '
                ) or 'stream'
            self.print_header('profile_user_header')
            profile_user = input(
                'Press return for the default awscli profile. [default] '
                ) or 'default'
            self.print_header('credential_format_header')
            credential_format = input(
                'Which credential format would you like to generate? [vault] '
                ) or 'vault'
        else:
            return
        parameters = {
            'log_mode': log_mode,
            'profile_user': profile_user,
            'credential_format': credential_format
        }
        self.create(cfg, parameters)

    def create(self, cfg, parameter_dict=None):
        """ create new config file """
        with open(cfg, 'w') as f1:
            f1.write(config_seed)
            f1.close()
        if parameter_dict:
            config_obj = ReadConfig(local_file=cfg)
            yml_object = config_obj.load()
            yml_object['LocalConfiguration']['logging']['log_mode'] = parameter_dict['log_mode']
            yml_object['LocalConfiguration']['profile_user'][0]['Default'] = parameter_dict['profile_user']
            yml_object['LocalConfiguration']['CredentialFormat'][0]['Default'] = parameter_dict['credential_format']
            with open(cfg, 'w') as yaml_file:
                yaml_file.write(yaml.dump(yml_object, default_flow_style=True))
        return

    def print_header(self, header):
        """ prints header strings to stdout """
        update_header = """
                     -- stsAval Local Configuration Setup --

        You will be asked a series of questions which will ask you to customize
        the input values for the stsAval library or accept the global defaults.

        Press return to accept the defaults shown in brackets [] at the end of
        each question.

        Type "Y" when you are ready to begin.
        """
        profile_user_header = """
        What is the name of the IAM account that will be used to generate
        temporary credentials for roles?
        """
        credential_format_header = """
        Which credential format would you like to generate, vault format
        (the default) or the native boto format?
        """
        if header == 'update_header':
            print(update_header)
        elif header == 'profile_user_header':
            print(profile_user_header)
        elif header == 'credentials_format_header':
            print(credentials_format_header)
        return


class ReadConfig():
    def __init__(self, local_file=''):
        if os.path.exists(local_file):
            self.local_file=local_file
        else:
            logger.info('local config file [%s] not found' % config_file)
            return {}

    def read(self, cfg=''):
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

    def load(self, cfg=''):
        """ returns object from yaml file """
        if not cfg:
            cfg = self.local_file
        with open(cfg, 'r') as stream:
            try:
                return yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)


if __name__ == '__main__':
    if os.path.exists(config_file):
        UpdateConfig(local_file=global_config['config_file'])
    else:
        config_obj = UpdateConfig(local_file=global_config['config_file'])
        config_obj.update(cfg=global_config['config_file'])
