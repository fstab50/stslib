config_seed = """
# -----------------------------------------------------------------------------
#        stsAval Configuration File Defaults
# -----------------------------------------------------------------------------

LocalConfiguration:
    logging:
        log_mode: 'file'
        log_dir: '~/.stsaval'
        log_file: 'stsaval.log'

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
