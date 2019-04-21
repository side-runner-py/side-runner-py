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


def test_call_with_argname_bind_pos_with_default_match():
    def _func(foo=-1, bar=-1):
        return foo, bar

    ret = utils.call_with_argname_bind(_func, {'foo': 0, 'bar': 1})
    assert ret == (0, 1)


def test_call_with_argname_bind_pos_with_default_mismatch():
    def _func(foo=-1, bar=-1):
        return foo, bar

    ret = utils.call_with_argname_bind(_func, {'foo': 0, 'buz': 2})
    assert ret == (-1, -1)


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
