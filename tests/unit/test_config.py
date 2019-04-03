import os
from unittest import mock
from side_runner_py import config


def test_default_config():
    os.environ['FOOBAR_CONFIG'] = ""
    with mock.patch.dict(config.CONFIG_MAP, {'foobar-config': {'value': 'foobar'}}, clear=True):
        config.Config.init()
        assert config.Config.FOOBAR_CONFIG == "foobar"


def test_env_overwrite_default_config():
    os.environ['FOOBAR_CONFIG'] = "env-foobar"
    with mock.patch.dict(config.CONFIG_MAP, {'foobar-config': {'value': 'default-foobar'}}, clear=True):
        config.Config.init()
        assert config.Config.FOOBAR_CONFIG == "env-foobar"


def test_arg_overwrite_default_config():
    os.environ['FOOBAR_CONFIG'] = "env-foobar"
    with mock.patch.object(config.sys, 'argv', ['prog_name', '--foobar-config=foobar']):
        with mock.patch.dict(config.CONFIG_MAP, {'foobar-config': {'value': 'default-foobar'}}, clear=True):
            config.Config.init()
            assert config.Config.FOOBAR_CONFIG == "foobar"


def test_config_type_cast_mixed():
    config_map = {
      'env-foobar-config': {'value': 'default-foobar', 'type': int},
      'env-foobar-config2': {'value': 'default-foobar', 'type': str},
      'arg-foobar-config': {'value': 'default-foobar', 'type': int}
    }
    os.environ['ENV_FOOBAR_CONFIG'] = "1"
    os.environ['ENV_FOOBAR_CONFIG2'] = "2"
    with mock.patch.object(config.sys, 'argv', ['prog_name', '--arg-foobar-config=3']):
        with mock.patch.dict(config.CONFIG_MAP, config_map, clear=True):
            config.Config.init()
            assert config.Config.ENV_FOOBAR_CONFIG == 1
            assert config.Config.ENV_FOOBAR_CONFIG2 == "2"
            assert config.Config.ARG_FOOBAR_CONFIG == 3
            assert type(config.Config.ENV_FOOBAR_CONFIG) == int
            assert type(config.Config.ENV_FOOBAR_CONFIG2) == str
            assert type(config.Config.ARG_FOOBAR_CONFIG) == int


def test_config_type_cast():
    config_map = {
      'env-foobar-config': {'value': 'default-foobar', 'type': int},
      'arg-foobar-config': {'value': 'default-foobar', 'type': int}
    }
    os.environ['ENV_FOOBAR_CONFIG'] = "1"
    with mock.patch.object(config.sys, 'argv', ['prog_name', '--arg-foobar-config=2']):
        with mock.patch.dict(config.CONFIG_MAP, config_map, clear=True):
            config.Config.init()
            assert config.Config.ENV_FOOBAR_CONFIG == 1
            assert config.Config.ARG_FOOBAR_CONFIG == 2
            assert type(config.Config.ENV_FOOBAR_CONFIG) == int
            assert type(config.Config.ARG_FOOBAR_CONFIG) == int


def test_config_type_default_cast():
    config_map = {
      'env-foobar-config': {'value': 'default-foobar'},
      'arg-foobar-config': {'value': 'default-foobar'}
    }
    os.environ['ENV_FOOBAR_CONFIG'] = "1"
    with mock.patch.object(config.sys, 'argv', ['prog_name', '--arg-foobar-config=2']):
        with mock.patch.dict(config.CONFIG_MAP, config_map, clear=True):
            config.Config.init()
            assert config.Config.ENV_FOOBAR_CONFIG == "1"
            assert config.Config.ARG_FOOBAR_CONFIG == "2"
            assert type(config.Config.ENV_FOOBAR_CONFIG) == str
            assert type(config.Config.ARG_FOOBAR_CONFIG) == str
