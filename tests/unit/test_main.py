import pytest
import os
from side_runner_py import main


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
