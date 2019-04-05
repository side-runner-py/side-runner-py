import json
from unittest import mock
import pytest
import os
from side_runner_py import main, config


def test_get_side_file_list_by_glob():
    with pytest.raises(ValueError):
        assert list(main._get_side_file_list_by_glob('')) == []


def test_get_side_fixed_file_list_by_glob(tmp_path):
    sidefile = tmp_path / "a.json"
    sidefile.write_text("[]")
    assert len(list(main._get_side_file_list_by_glob(str(sidefile)))) == 1


def test_main_with_glob_no_match(mocker):
    mocker.patch('side_runner_py.main.with_retry')
    os.environ["SIDE_FILE"] = "foobar_not_existed_filename.side"
    execute_side_file_mock = mocker.patch('side_runner_py.main._execute_side_file')
    main.main()
    assert execute_side_file_mock.call_count == 0


def test_main_failed_session_close(mocker, tmp_path):
    mocker.patch('side_runner_py.main.with_retry')
    mocker.patch('side_runner_py.main.get_screenshot')
    mocker.patch('side_runner_py.main.execute_test_command', side_effect=Exception('foobar'))
    driver_close = mocker.patch('side_runner_py.main.SessionManager._close_driver_or_skip')

    # parepare mock test file
    sidefile_a = tmp_path / "a.json"
    orig_test_project_a = {
        'suites': [{'id': 'foobar_a', 'tests': ['foobar_a']}],
        'tests': [{'id': 'foobar_a', 'commands': [{}]}], 'id': 'foobar_a'
    }
    sidefile_a.write_text(json.dumps(orig_test_project_a))

    # call main with mocked driver, etc...
    with mock.patch.object(config.sys, 'argv', ['prog_name', '--side-file={}'.format(tmp_path/"*.json")]):
        main.main()
        # driver close called at failure-test, test-suite, tests end
        assert driver_close.call_count == 3


def test_main_persistent_session(mocker, tmp_path):
    mocker.patch('side_runner_py.main.with_retry')
    mocker.patch('side_runner_py.main.get_screenshot')
    mocker.patch('side_runner_py.main.execute_test_command').return_value = {'is_failed': False}
    driver_close = mocker.patch('side_runner_py.main.SessionManager._close_driver_or_skip')

    # parepare mock test file
    sidefile_a = tmp_path / "a.json"
    orig_test_project_a = {
        'id': 'foobar_a',
        'suites': [{'name': 'foobar_a', 'id': 'foobar_a', 'tests': ['foobar_a'], 'persistSession': True}],
        'tests': [
            {'name': 'foobar_a', 'id': 'foobar_a',
                'commands': [{'command': 'foobar', 'target': 'foobar', 'value': 'foobar'}]}
        ],
    }
    sidefile_a.write_text(json.dumps(orig_test_project_a))

    # call main with mocked driver, etc...
    with mock.patch.object(config.sys, 'argv', ['prog_name', '--side-file={}'.format(tmp_path/"*.json")]):
        main.main()
        # driver close called at test-suite end
        assert driver_close.call_count == 1


def test_main_non_persistent_session(mocker, tmp_path):
    mocker.patch('side_runner_py.main.with_retry')
    mocker.patch('side_runner_py.main.get_screenshot')
    mocker.patch('side_runner_py.main.execute_test_command').return_value = {'is_failed': False}
    driver_close = mocker.patch('side_runner_py.main.SessionManager._close_driver_or_skip')

    # parepare mock test file
    sidefile_a = tmp_path / "a.json"
    orig_test_project_a = {
        'id': 'foobar_a',
        'suites': [{'name': 'foobar_a', 'id': 'foobar_a', 'tests': ['foobar_a'], 'persistSession': False}],
        'tests': [
            {'name': 'foobar_a', 'id': 'foobar_a',
                'commands': [{'command': 'foobar', 'target': 'foobar', 'value': 'foobar'}]}
        ],
    }
    sidefile_a.write_text(json.dumps(orig_test_project_a))

    # call main with mocked driver, etc...
    with mock.patch.object(config.sys, 'argv', ['prog_name', '--side-file={}'.format(tmp_path/"*.json")]):
        main.main()
        # driver close called at test-suite, tests end
        assert driver_close.call_count == 2


def test_main_multiple_not_shared(mocker, tmp_path):
    mocker.patch('side_runner_py.main.with_retry')
    mocker.patch('side_runner_py.main.get_screenshot')
    mocker.patch('side_runner_py.main.execute_test_command')

    # parepare mock test file
    sidefile_a = tmp_path / "a.json"
    orig_test_project_a = {
        'suites': [{'id': 'foobar_a', 'tests': ['foobar_a']}],
        'tests': [{'id': 'foobar_a', 'commands': []}], 'id': 'foobar_a'
    }
    sidefile_a.write_text(json.dumps(orig_test_project_a))
    sidefile_b = tmp_path / "b.json"
    orig_test_project_b = {
        'suites': [{'id': 'foobar_b', 'tests': ['foobar_b']}],
        'tests': [{'id': 'foobar_b', 'commands': []}], 'id': 'foobar_b'
    }
    sidefile_b.write_text(json.dumps(orig_test_project_b))

    # call main with mocked driver, etc...
    with mock.patch.object(config.sys, 'argv', ['prog_name', '--side-file={}'.format(tmp_path/"*.json")]):
        main.main()


def test_main_multiple_shared(mocker, tmp_path):
    mocker.patch('side_runner_py.main.with_retry')
    mocker.patch('side_runner_py.main.get_screenshot')
    mocker.patch('side_runner_py.main.execute_test_command')

    # parepare mock test file
    sidefile_a = tmp_path / "a.json"
    orig_test_project_a = {
        'suites': [{'id': 'foobar_a', 'tests': ['foobar_a']}],
        'tests': [{'id': 'foobar_a', 'commands': []}], 'id': 'foobar_a'
    }
    sidefile_a.write_text(json.dumps(orig_test_project_a))
    sidefile_b = tmp_path / "b.json"
    orig_test_project_b = {
        'suites': [{'id': 'foobar_b', 'tests': ['foobar_a', 'foobar_b']}],
        'tests': [{'id': 'foobar_b', 'commands': []}], 'id': 'foobar_b'
    }
    sidefile_b.write_text(json.dumps(orig_test_project_b))

    # call main with mocked driver, etc...
    with mock.patch.object(config.sys, 'argv', ['prog_name', '--side-file={}'.format(tmp_path/"*.json")]):
        main.main()
