import logging
from logging import basicConfig, INFO
from time import strftime, gmtime
from .config import Config

FORMAT = '{asctime} {levelname} {name}: {message}'
DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
basicConfig(level=INFO, format=FORMAT, datefmt=DATE_FORMAT, style='{')


class JoinFormatter:
    def format(recode):
        items = [recode.msg]
        items.extend(recode.args)
        recode.__dict__['message'] = ' '.join([str(item) for item in items])
        recode.__dict__['asctime'] = strftime(DATE_FORMAT, gmtime(recode.created))
        return FORMAT.format(**recode.__dict__)


def getLogger(name):
    logger = logging.getLogger(name)
    logger.propagate = False

    Config.init(suppress_logging=True)
    log_level = getattr(logging, Config.LOG_LEVEL)
    logger.setLevel(log_level)

    handler = logging.StreamHandler()
    handler.setFormatter(JoinFormatter)
    logger.addHandler(handler)

    return logger
