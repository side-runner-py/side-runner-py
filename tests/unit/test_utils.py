import re
import pytest
from side_runner_py import utils


def test_call_with_argname_bind_pos_match():
    def _func(foo, bar):
        return foo, bar

    ret = utils.call_with_argname_bind(_func, {'foo': 0, 'bar': 1})
    assert ret == (0, 1)


def test_call_with_argname_bind_pos_mismatch():
    def _func(foo, bar):
        return foo, bar

    ret = utils.call_with_argname_bind(_func, {'foo': 0, 'buz': 2})
    assert ret is None


def test_call_with_argname_bind_pos_partial_match():
    def _func(foo):
        return foo

    ret = utils.call_with_argname_bind(_func, {'foo': 0, 'bar': 1})
    assert ret == 0


def test_call_with_argname_bind_pos_with_default_match():
    def _func(foo=-1, bar=-1):
        return foo, bar

    ret = utils.call_with_argname_bind(_func, {'foo': 0, 'bar': 1})
    assert ret == (0, 1)


def test_call_with_argname_bind_pos_with_default_partial_match():
    def _func(foo=-1, bar=-1):
        return foo, bar

    ret = utils.call_with_argname_bind(_func, {'foo': 0, 'buz': 2})
    assert ret == (0, -1)


def test_call_with_argname_bind_no_arg():
    def _func():
        return 'foobar'

    ret = utils.call_with_argname_bind(_func, {'foo': 0, 'bar': 1})
    assert ret == 'foobar'


def test_call_with_argname_bind_kw_only():
    def _func(*args, foo=-1, bar=-1, **kwargs):
        return args, foo, bar, kwargs

    ret = utils.call_with_argname_bind(_func, {'foo': 0, 'bar': 1})
    assert ret == (tuple(), -1, -1, dict())


def test_construct_dict():
    ret = utils.construct_dict('goog:chromeOptions prefs intl.accept_languages', 'ja_JP')
    assert ret == {'goog:chromeOptions': {'prefs': {'intl.accept_languages': 'ja_JP'}}}


@pytest.mark.parametrize('regexp,s,result', [
    ('\\${KEY_([A-Z0-9]+)}', 'aaa', ['aaa']),
    ('\\${KEY_([A-Z0-9]+)}', '${KEY_UP}', ['UP']),
    ('\\${KEY_([A-Z0-9]+)}', 'a${KEY_UP}b', ['a', 'UP', 'b']),
    ('\\${KEY_([A-Z0-9]+)}', '${KEY_UP}a${KEY_DOWN}', ['UP', 'a', 'DOWN']),
    ('\\${KEY_([A-Z0-9]+)}', '${KEY_UP}aaa${KEY_DOWN}${KEY_ENTER}', ['UP', 'aaa', 'DOWN', 'ENTER']),
])
def test_split_with_re(regexp, s, result):
    def _(m):
        return m.group(1)

    ret = utils.split_with_re(re.compile(regexp), s, _)
    assert ret == result
