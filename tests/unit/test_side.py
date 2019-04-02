import pytest
from side_runner_py import side


def test_parse_empty_side_file(mocker):
    mocker.patch('side_runner_py.side.open')
    mocker.patch('json.load').return_value = {'suites': [], 'tests': []}
    side.parse_side('foobar.side')


def test_parse_invalid_side_file(mocker):
    mocker.patch('side_runner_py.side.open')
    mocker.patch('json.load').return_value = {}

    with pytest.raises(KeyError):
        side.parse_side('foobar.side')


def test_attach_empty_params(mocker):
    mocker.patch('side_runner_py.side.open')
    mocker.patch('json.load').return_value = {}

    tests = []
    side.attach_params('foobar.json', tests)
    assert tests == []


def test_attach_params(mocker):
    params = [
        {
            "test_name": "Input form",
            "params_type": "list",
            "params": [
                {"message": "Foo"},
                {"message": "Bar"}
            ]
        },
    ]
    mocker.patch('side_runner_py.side.open')
    mocker.patch('json.load').return_value = params

    tests = {'foobar': {"id": "foobar", "name": "Input form"}}
    side.attach_params('foobar.json', tests)

    assert 'params' in tests['foobar']
    assert tests['foobar']['params'] == params[0]['params']
