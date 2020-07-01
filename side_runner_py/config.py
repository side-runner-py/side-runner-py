import sys
import yaml
import stingconf
from logging import getLogger
logger = getLogger(__name__)


CONFIG_YAML = '''
env_prefix: SIDE
order:
  - arg
  - env
  - default
items:
  webdriver-url:
    default: http://webdriver:4444/wd/hub
  test-file:
    default: [default.side]
    repeatable: true
  http-proxy:
    default: ''
    env:
      no_prefix: true
      ignorecase: true
  https-proxy:
    default: ''
    env:
      no_prefix: true
      ignorecase: true
  no-proxy:
    default: ''
    env:
      no_prefix: true
      ignorecase: true
  output-dir:
    default: ./output
  desired-capabilities:
    default: []
    repeatable: true
    arg:
      short: c
  driver-retry-count:
    default: 5
    type: int
  driver-retry-wait:
    default: 5
    type: int
  driver-element-wait:
    default: 10
    type: int
  driver-command-wait:
    default: 0
    type: int
  hook-scripts-dir:
    default: hooks
  log-level:
    default: INFO
  close-method:
    default: close
'''

CONFIG_DEF = yaml.safe_load(CONFIG_YAML)


class Config:
    @staticmethod
    def init(suppress_logging=False):
        parser = stingconf.Parser('Execute Selenium IDE (.side) tests', CONFIG_DEF)
        config = parser.parse(sys.argv[1:])
        for k, v in config.items():
            setattr(Config, k, v)
            if not suppress_logging:
                logger.info("Config.{}: = {}".format(k, v))
