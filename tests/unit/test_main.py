import pytest
import os
from side_runner_py import main


def test_get_side_file_list_by_glob():
    with pytest.raises(ValueError):
        assert list(main._get_side_file_list_by_glob('')) == []


def test_get_side_fixed_file_list_by_glob():
    assert list(main._get_side_file_list_by_glob('/tmp/a.json')) == ['/tmp/a.json']


def test_main_with_glob_no_match(mocker):
    mocker.patch('side_runner_py.main.with_retry')
    os.environ["SIDE_FILE"] = "foobar_not_existed_filename.side"
    execute_side_file_mock = mocker.patch('side_runner_py.main._execute_side_file')
    main.main()
    assert execute_side_file_mock.call_count == 0


def test_main_with_glob_one_match(mocker):
    mocker.patch('side_runner_py.main.with_retry')
    mocker.patch('side_runner_py.main.SIDEProjectManager')

    path_file_mock = mocker.Mock()
    path_file_mock.stem = "foobar-1"
    path_mock = mocker.Mock()
    path_mock.parent.glob.return_value = [path_file_mock]
    mocker.patch('side_runner_py.main.pathlib.Path').return_value = path_mock

    execute_side_file_mock = mocker.patch('side_runner_py.main._execute_side_file')
    main.main()
    assert execute_side_file_mock.call_count == 1


def test_main_with_glob_multi_match(mocker):
    mocker.patch('side_runner_py.main.with_retry')
    mocker.patch('side_runner_py.main.SIDEProjectManager')

    path_file_mock = mocker.Mock()
    path_file_mock.stem = "foobar-1"
    path_mock = mocker.Mock()
    path_mock.parent.glob.return_value = [path_file_mock, path_file_mock]
    mocker.patch('side_runner_py.main.pathlib.Path').return_value = path_mock

    execute_side_file_mock = mocker.patch('side_runner_py.main._execute_side_file')
    main.main()
    assert execute_side_file_mock.call_count == 2
