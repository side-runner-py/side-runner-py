import os
import argparse
from logging import getLogger
logger = getLogger(__name__)


def _update_or_skip(target, key, data=None, default=None):
    if not hasattr(target, key):
        setattr(target, key, default)
    if data:
        setattr(target, key, data)
    elif not data and default:
        setattr(target, key, default)
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
    'driver-command-wait': {'value': 0, 'type': int},
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
        args = parser.parse_args()

        # set each config value from default, env, cmd
        for key, default in CONFIG_MAP.items():
            env_key = key.replace('-', '_').upper()
            setattr(Config, env_key, default['value'])
            _update_or_skip(Config, env_key, os.environ.get(env_key), None)
            _update_or_skip(Config, env_key, getattr(args, env_key), None)
            logger.info("Config.{}: = {}".format(env_key, getattr(Config, env_key)))
