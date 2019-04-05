import os
from unittest import mock
from side_runner_py import config


def test_default_config():
    os.environ.pop('SIDE_FOOBAR_CONFIG', None)
    with mock.patch.dict(config.CONFIG_DEF['items'], {'foobar-config': {'default': 'default-foobar'}}, clear=True):
        config.Config.init()
        assert config.Config.FOOBAR_CONFIG == "default-foobar"


def test_env_overwrite_default_config():
    os.environ['SIDE_FOOBAR_CONFIG'] = "env-foobar"
    with mock.patch.dict(config.CONFIG_DEF['items'], {'foobar-config': {'default': 'default-foobar'}}, clear=True):
        config.Config.init()
        assert config.Config.FOOBAR_CONFIG == "env-foobar"


def test_arg_overwrite_default_config():
    os.environ['SIDE_FOOBAR_CONFIG'] = "env-foobar"
    with mock.patch.object(config.sys, 'argv', ['prog_name', '--foobar-config=arg-foobar']):
        with mock.patch.dict(config.CONFIG_DEF['items'], {'foobar-config': {'default': 'default-foobar'}}, clear=True):
            config.Config.init()
            assert config.Config.FOOBAR_CONFIG == "arg-foobar"
