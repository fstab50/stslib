"""
Summary:
    local yaml configuration file template

Args:
    config_seed (str):  file template

Returns:
    None
"""

config_seed = """
# -----------------------------------------------------------------------------
#        stslib Configuration File Defaults
# -----------------------------------------------------------------------------

LocalConfiguration:
    logging:
        log_mode: 'file'
        log_dir: '~/.stslib'
        log_file: 'stslib.log'

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
