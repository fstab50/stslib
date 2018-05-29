#!/usr/bin/env python3
""" refactor Module Level comments NEEDED HERE

Module Attributes:
    logger - logging object


"""

import os
import json
import configparser
import sys
import argparse
import inspect
from stslib import logd
from stslib.statics import defaults, global_config
from stslib._version import __version__


logger = logd.getLogger(__version__)


# Module Attributes
config_dir = defaults['config_path']
prefix = global_config['credential_prefix']
prefix_alt = global_config['alternate_prefix']


# -- function declarations  ---------------------------------------------------

def parse_awscli(parameter_input=None, parameter_output=None):
    """
    Summary:
        imports awscli credentials file, refactors format to json

    Args:
        parameter_input: TYPE: string, opt input file if not awscli default
        parameter_output: TYPE: string, opt ouput file if not stslib default

    Returns:
        Success or Failure, TYPE: Boolean
    """
    # input file - to be parsed
    awscli_file = parameter_input or defaults['default_awscli']
    # ouput file - after parsing
    if config_dir in parameter_output:
        output_file = (parameter_output or defaults['output_file'])
    else:
        output_file = config_dir + '/' + (parameter_output or defaults['output_file'])

    logger.info('awscli_file (input) is: %s' % awscli_file)
    logger.info('output_file is: %s' % output_file)

    total_dict, tmp = {}, {}

    if not os.path.exists(awscli_file):
        logger.info(
            'awscli credentials or provided file input [%s] missing. Abort' %
            awscli_file
        )
        return False
    elif not os.path.exists(config_dir):
        logger.info('Configuration dir [%s] missing, creating it' % config_dir)
        os.mkdir(config_dir)

    config = configparser.ConfigParser()
    config.read(awscli_file)

    iam_keys = ['aws_access_key_id', 'aws_secret_access_key']
    role_keys = ['role_arn', 'mfa_serial', 'source_profile']

    filtered_list = list(filter(lambda x: prefix_alt not in x,
                        filter(lambda x: prefix not in x, config.sections())))

    try:
        for profile in filtered_list:
            if set(iam_keys).issubset(config[profile].keys()):
                for key in iam_keys:
                    tmp[key] = config[profile][key]
                if 'mfa_serial' in config[profile].keys():    # mfa secured cli
                    tmp['mfa_serial'] = config[profile]['mfa_serial']

            elif set(role_keys).issubset(config[profile].keys()):
                for key in role_keys:
                    tmp[key] = config[profile][key]

            total_dict[profile] = tmp
            tmp = {}

        # write output file
        with open(output_file, 'w') as f2:
            f2.write(json.dumps(total_dict, indent=4))
            f2.close()

        # secure file permissions
        os.chmod(output_file, 0o700)

    except KeyError as e:
        logger.critical(
            '%s: Cannot find Key %s while parsing file %s' %
            (inspect.stack()[0][3], str(e), input_file))
        return False
    except OSError as e:
        logger.critical(
            '%s: problem opening file %s. Error %s' %
            (inspect.stack()[0][3], awscli_file, str(e)))
        return False
    except Exception as e:
        logger.critical(
            '%s: Unknown error. Error %s' %
            (inspect.stack()[0][3], str(e)))
        raise e
    return True


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='stslib credential data build')
    parser.add_argument("-i", "--input", help="awscli format Input File", required=False)
    parser.add_argument("-o", "--output", help="Credential Output File", required=False)
    parser.add_argument("--defaults", help="Use default awscli files", action="store_true")
    args = parser.parse_args()


    if args.input is None and args.output is None:
        if args.defaults:
            # refactor awscli credentials using defaults
            parse_awscli()

        elif len(sys.argv) == 2:
            parser.print_help()
            logger.warning(
                '\nUse of default awscli files requires only "--defaults"\n'
            )
            sys.exit(0)

    else:
        # specify non-default input, output files
        input_file = args.input
        output_file = args.output
        # refactor using defaults with manual input
        parse_awscli(parameter_input=input_file, parameter_output=output_file)
