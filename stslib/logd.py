"""
Project-level logging module

"""
import logging
import datetime
from stslib.statics import global_config




def getLogger(*args, **kwargs):
    """
    Summary:
        custom format logger

    Args:
        __version__: global var, project level
        log_mode:  stream | file output format

    Returns:
        logger object | TYPE: logging
    """
    # args
    log_mode = kwargs.get('log_mode', global_config['log_mode'])
    logger = logging.getLogger(*args, **kwargs)
    logger.propagate = False

    try:
        if not logger.handlers:
            # branch on output format, default to stream
            if log_mode == 'file' or log_mode == 'File':
                # file handler
                f_handler = logging.FileHandler(global_config['log_file'])
                f_formatter = logging.Formatter('%(asctime)s - %(pathname)s - %(name)s - [%(levelname)s]: %(message)s')
                #f_formatter = logging.Formatter('%(asctime)s %(processName)-10s %(name)s [%(levelname)-5s]: %(message)s')
                f_handler.setFormatter(f_formatter)
                logger.addHandler(f_handler)
            elif log_mode == 'stream' or log_mode == 'stdout':
                # stream handlers
                s_handler = logging.StreamHandler()
                s_formatter = logging.Formatter('%(pathname)s - %(name)s - [%(levelname)s]: %(message)s')
                s_handler.setFormatter(s_formatter)
                logger.addHandler(s_handler)
            else:
                logger.addHandler(f_handler)
                logger.addHandler(s_handler)
            logger.setLevel(logging.DEBUG)
    except OSError as e:
        raise e
    return logger
