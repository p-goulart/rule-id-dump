import logging
from sys import stdout


# TODO: make proper formatter
def logger_wrapper(name, level):
    logger = logging.Logger(name)
    logger.addHandler(logging.StreamHandler(stdout))
    logger.setLevel(level)
    return logger
