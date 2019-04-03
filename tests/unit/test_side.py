import pytest
from side_runner_py.side import SIDEProjectManager


class TestSIDEProjectManager:
    def test_parse_empty_side_file(self, mocker):
        mocker.patch('side_runner_py.side.open')
        mocker.patch('json.load').return_value = {'id': 'foobar', 'suites': [], 'tests': []}
        side_manager = SIDEProjectManager()
        side_manager.add_project('foobar.side', 'foobar_params.json')

    def test_parse_invalid_side_file(self, mocker):
        mocker.patch('side_runner_py.side.open')
        mocker.patch('json.load').return_value = {}

        with pytest.raises(KeyError):
            side_manager = SIDEProjectManager()
            side_manager.add_project('foobar.side', 'foobar_params.json')

    def test_attach_empty_params(self, mocker):
        mocker.patch('side_runner_py.side.open')
        mocker.patch('json.load').return_value = {}

        tests = []
        side_manager = SIDEProjectManager()
        side_manager._attach_params('foobar.json', tests)
        assert tests == []

    def test_attach_params(self, mocker):
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
        side_manager = SIDEProjectManager()
        side_manager._attach_params('foobar.json', tests)

        assert 'params' in tests['foobar']
        assert tests['foobar']['params'] == params[0]['params']

    def test_expand_test_with_params(self, mocker):
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
        side_manager = SIDEProjectManager()
        side_manager._attach_params('foobar.json', tests)
        test_suites = [{'id': 'foobar', 'tests': ['foobar'], 'name': 'foobar'}]
        test_suites, tests = side_manager._expand_test_with_params(test_suites, tests)
        assert test_suites == [
            {'id': 'foobar-0', 'name': 'foobar-0', 'tests': ['foobar-0']},
            {'id': 'foobar-1', 'name': 'foobar-1', 'tests': ['foobar-1']}]
        assert tests == {
            'foobar-0': {
                'id': 'foobar-0',
                'name': 'Input form-0',
                'params': [{'message': 'Foo'}, {'message': 'Bar'}]
            },
            'foobar-1': {
                'id': 'foobar-1',
                'name': 'Input form-1',
                'params': [{'message': 'Foo'}, {'message': 'Bar'}]
            }}
