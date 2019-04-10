import pytest
from side_runner_py import hook


def _create_hook_mock(mocker, conditions, func_name):
    hook_mock = mocker.Mock()
    hook_func = mocker.Mock()
    setattr(hook_mock, '__name__', 'dummy_hook')
    setattr(hook_mock, 'conditions', conditions)
    setattr(hook_mock, func_name, hook_func)
    return hook_mock, hook_func


@pytest.mark.parametrize('pre_or_post,kind,argc', [
    ('pre', 'project', 1),
    ('pre', 'suite', 2),
    ('pre', 'test', 3),
    ('post', 'project', 1),
    ('post', 'suite', 2),
    ('post', 'test', 3),
])
def test_call_hook_any_cases(mocker, pre_or_post, kind, argc):
    # prepare hook mock
    conditions = {
        'test_project_ids': ['*'],
        'test_suite_ids': ['*'],
        'test_ids': ['*'],
    }
    hook_mock, hook_func = _create_hook_mock(mocker, conditions, '{}_{}_run'.format(pre_or_post, kind))
    mocker.patch('side_runner_py.hook.Config')
    mocker.patch('side_runner_py.hook.load_hook_scripts').return_value = [hook_mock]

    # call hook
    ids = [{'id': '', 'name': ''} for i in range(argc)]
    f = getattr(hook, 'run_hook_per_' + kind)
    f(pre_or_post, *ids)
    assert hook_func.call_count == 1


def test_filter_hook_by_project_id(mocker):
    # prepare hook mock
    conditions = {
        'test_project_ids': ['ID1'],
    }
    hook_mock, hook_func = _create_hook_mock(mocker, conditions, 'pre_project_run')
    mocker.patch('side_runner_py.hook.Config')
    mocker.patch('side_runner_py.hook.load_hook_scripts').return_value = [hook_mock]

    # call hook
    hook.run_hook_per_project('pre', {'id': 'ID1', 'name': ''})
    assert hook_func.call_count == 1

    hook.run_hook_per_project('pre', {'id': 'ID2', 'name': ''})
    assert hook_func.call_count == 1


def test_filter_hook_by_project_name(mocker):
    # prepare hook mock
    conditions = {
        'test_project_names': ['Foo'],
    }
    hook_mock, hook_func = _create_hook_mock(mocker, conditions, 'pre_project_run')
    mocker.patch('side_runner_py.hook.Config')
    mocker.patch('side_runner_py.hook.load_hook_scripts').return_value = [hook_mock]

    # call hook
    hook.run_hook_per_project('pre', {'id': '', 'name': 'Foo'})
    assert hook_func.call_count == 1

    hook.run_hook_per_project('pre', {'id': '', 'name': 'Bar'})
    assert hook_func.call_count == 1


def test_filter_hook_by_suite_id(mocker):
    # prepare hook mock
    conditions = {
        'test_project_ids': ['*'],
        'test_suite_ids': ['ID1'],
    }
    hook_mock, hook_func = _create_hook_mock(mocker, conditions, 'pre_suite_run')
    mocker.patch('side_runner_py.hook.Config')
    mocker.patch('side_runner_py.hook.load_hook_scripts').return_value = [hook_mock]

    # call hook
    hook.run_hook_per_suite('pre', {'id': 'ID1', 'name': ''}, {'id': 'ID1', 'name': ''})
    assert hook_func.call_count == 1

    hook.run_hook_per_suite('pre', {'id': 'ID1', 'name': ''}, {'id': 'ID2', 'name': ''})
    assert hook_func.call_count == 1

    hook.run_hook_per_suite('pre', {'id': 'ID2', 'name': ''}, {'id': 'ID1', 'name': ''})
    assert hook_func.call_count == 2


def test_filter_hook_by_suite_name(mocker):
    # prepare hook mock
    conditions = {
        'test_project_names': ['*'],
        'test_suite_names': ['Foo Suite'],
    }
    hook_mock, hook_func = _create_hook_mock(mocker, conditions, 'pre_suite_run')
    mocker.patch('side_runner_py.hook.Config')
    mocker.patch('side_runner_py.hook.load_hook_scripts').return_value = [hook_mock]

    # call hook
    hook.run_hook_per_suite('pre', {'id': '', 'name': 'Foo'}, {'id': '', 'name': 'Foo Suite'})
    assert hook_func.call_count == 1

    hook.run_hook_per_suite('pre', {'id': '', 'name': 'Foo'}, {'id': '', 'name': 'Bar Suite'})
    assert hook_func.call_count == 1

    hook.run_hook_per_suite('pre', {'id': '', 'name': 'Bar'}, {'id': '', 'name': 'Foo Suite'})
    assert hook_func.call_count == 2


def test_filter_hook_by_test_id(mocker):
    # prepare hook mock
    conditions = {
        'test_project_ids': ['*'],
        'test_suite_ids': ['*'],
        'test_ids': ['ID1'],
    }
    hook_mock, hook_func = _create_hook_mock(mocker, conditions, 'pre_test_run')
    mocker.patch('side_runner_py.hook.Config')
    mocker.patch('side_runner_py.hook.load_hook_scripts').return_value = [hook_mock]

    # call hook
    hook.run_hook_per_test('pre', {'id': 'ID1', 'name': ''}, {'id': 'ID1', 'name': ''}, {'id': 'ID1', 'name': ''})
    assert hook_func.call_count == 1

    hook.run_hook_per_test('pre', {'id': 'ID1', 'name': ''}, {'id': 'ID1', 'name': ''}, {'id': 'ID2', 'name': ''})
    assert hook_func.call_count == 1

    hook.run_hook_per_test('pre', {'id': 'ID2', 'name': ''}, {'id': 'ID2', 'name': ''}, {'id': 'ID1', 'name': ''})
    assert hook_func.call_count == 2


def test_filter_hook_by_test_name(mocker):
    # prepare hook mock
    conditions = {
        'test_project_names': ['*'],
        'test_suite_names': ['*'],
        'test_names': ['Foo Test'],
    }
    hook_mock, hook_func = _create_hook_mock(mocker, conditions, 'pre_test_run')
    mocker.patch('side_runner_py.hook.Config')
    mocker.patch('side_runner_py.hook.load_hook_scripts').return_value = [hook_mock]

    # call hook
    hook.run_hook_per_test('pre', {'id': '', 'name': 'Foo'}, {'id': '', 'name': 'Foo'}, {'id': '', 'name': 'Foo Test'})
    assert hook_func.call_count == 1

    hook.run_hook_per_test('pre', {'id': '', 'name': 'Foo'}, {'id': '', 'name': 'Foo'}, {'id': '', 'name': 'Bar Test'})
    assert hook_func.call_count == 1

    hook.run_hook_per_test('pre', {'id': '', 'name': 'Bar'}, {'id': '', 'name': 'Bar'}, {'id': '', 'name': 'Foo Test'})
    assert hook_func.call_count == 2


def test_filter_hook_complexly(mocker):
    # prepare hook mock
    conditions = {
        'test_project_names': ['Foo'],
        'test_suite_names': ['Foo Suite'],
        'test_names': ['Foo Test'],
    }
    hook_mock, hook_func = _create_hook_mock(mocker, conditions, 'pre_test_run')
    mocker.patch('side_runner_py.hook.Config')
    mocker.patch('side_runner_py.hook.load_hook_scripts').return_value = [hook_mock]

    # call hook
    hook.run_hook_per_test('pre', {'id': '', 'name': 'Foo'}, {'id': '', 'name': 'Foo Suite'}, {'id': '', 'name': 'Foo Test'})
    assert hook_func.call_count == 1

    hook.run_hook_per_test('pre', {'id': '', 'name': 'Bar'}, {'id': '', 'name': 'Foo Suite'}, {'id': '', 'name': 'Foo Test'})
    assert hook_func.call_count == 1

    hook.run_hook_per_test('pre', {'id': '', 'name': 'Foo'}, {'id': '', 'name': 'Bar Suite'}, {'id': '', 'name': 'Foo Test'})
    assert hook_func.call_count == 1

    hook.run_hook_per_test('pre', {'id': '', 'name': 'Foo'}, {'id': '', 'name': 'Foo Suite'}, {'id': '', 'name': 'Bar Test'})
    assert hook_func.call_count == 1


def test_never_call_hook_per_suite(mocker):
    # prepare hook mock
    conditions = {
        'test_suite_names': ['Foo Suite'],
    }
    hook_mock, hook_func = _create_hook_mock(mocker, conditions, 'pre_suite_run')
    mocker.patch('side_runner_py.hook.Config')
    mocker.patch('side_runner_py.hook.load_hook_scripts').return_value = [hook_mock]

    # call hook
    hook.run_hook_per_suite('pre', {'id': '', 'name': 'Foo'}, {'id': '', 'name': 'Foo Suite'})
    assert hook_func.call_count == 0

    hook.run_hook_per_suite('pre', {'id': '', 'name': 'Bar'}, {'id': '', 'name': 'Foo Suite'})
    assert hook_func.call_count == 0


def test_never_call_hook_per_test(mocker):
    # prepare hook mock
    conditions = {
        'test_names': ['Foo Test'],
    }
    hook_mock, hook_func = _create_hook_mock(mocker, conditions, 'pre_test_run')
    mocker.patch('side_runner_py.hook.Config')
    mocker.patch('side_runner_py.hook.load_hook_scripts').return_value = [hook_mock]

    # call hook
    hook.run_hook_per_test('pre', {'id': '', 'name': 'Foo'}, {'id': '', 'name': 'Foo Suite'}, {'id': '', 'name': 'Foo Test'})
    assert hook_func.call_count == 0

    hook.run_hook_per_test('pre', {'id': '', 'name': 'Bar'}, {'id': '', 'name': 'Bar Suite'}, {'id': '', 'name': 'Foo Test'})
    assert hook_func.call_count == 0
