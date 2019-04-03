import sys
import os
import argparse
from logging import getLogger
logger = getLogger(__name__)


def _cast_or_raw(value, type_class):
    if value:
        return type_class(value)
    return value


def _update_or_skip(target, key, data=None):
    if not hasattr(target, key):
        setattr(target, key, None)
    if data:
        setattr(target, key, data)
    else:
        return


CONFIG_MAP = {
    'webdriver-url': {'value': 'http://webdriver:4444/wd/hub'},
    'side-file': {'value': 'default.side'},
    'param-file': {'value': 'param.json'},
    'http-proxy': {'value': ''},
    'https-proxy': {'value': ''},
    'no-proxy': {'value': ''},
    'output-dir': {'value': './output'},
    'driver-retry-count': {'value': 5, 'type': int},
    'driver-retry-wait': {'value': 5, 'type': int},
    'driver-element-wait': {'value': 10, 'type': int},
    'hook-scripts-dir': {'value': 'hooks'},
}


class Config:
    @staticmethod
    def init():
        # prepare cmdline arg parser
        parser = argparse.ArgumentParser(description='Execute Selenium IDE (.side) tests')
        for key, opt in CONFIG_MAP.items():
            type_class = opt.get('type', str)
            parser.add_argument('--{}'.format(key), dest=key.replace('-', '_').upper(), type=type_class)
        args = parser.parse_args(sys.argv[1:])

        # set each config value from default, env, cmd
        for key, default in CONFIG_MAP.items():
            env_key = key.replace('-', '_').upper()
            type_class = opt.get('type', str)
            setattr(Config, env_key, default['value'])
            _update_or_skip(Config, env_key, _cast_or_raw(os.environ.get(env_key), type_class))
            _update_or_skip(Config, env_key, _cast_or_raw(getattr(args, env_key), type_class))
            logger.info("Config.{}: = {}".format(env_key, getattr(Config, env_key)))
