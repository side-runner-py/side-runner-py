import json
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
        test_suites, tests = side_manager._expand_test_project_with_params(test_suites, tests)
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

    def test_add_project_once(self, tmp_path):
        sidefile = tmp_path / "a.json"
        orig_test_project = {'suites': [{'tests': ['foobar']}], 'tests': [{'id': 'foobar'}], 'id': 'foobar'}
        sidefile.write_text(json.dumps(orig_test_project))

        side_manager = SIDEProjectManager()
        side_manager.add_project(str(sidefile), None)

    def test_add_project_twice(self, tmp_path):
        sidefile_a = tmp_path / "a.json"
        sidefile_a.write_text(json.dumps({'suites': [], 'tests': [], 'id': 'foobar'}))

        sidefile_b = tmp_path / "b.json"
        sidefile_b.write_text(json.dumps({'suites': [], 'tests': [], 'id': 'foobar'}))

        side_manager = SIDEProjectManager()
        side_manager.add_project(str(sidefile_a), None)
        side_manager.add_project(str(sidefile_b), None)

    def test_get_project(self, tmp_path):
        sidefile = tmp_path / "a.json"
        orig_test_project = {'suites': [{'tests': ['foobar']}], 'tests': [{'id': 'foobar'}], 'id': 'foobar'}
        sidefile.write_text(json.dumps(orig_test_project))

        side_manager = SIDEProjectManager()
        project_id = side_manager.add_project(str(sidefile), None)
        test_project, test_suites, tests = side_manager.get_project(project_id)

        assert project_id == 'foobar'
        assert test_project == orig_test_project
        assert test_suites == orig_test_project['suites']
        assert tests == {'foobar': {'id': 'foobar'}}

    def test_get_project_shared(self, tmp_path):
        sidefile_a = tmp_path / "a.json"
        orig_test_project_a = {'suites': [{'tests': ['foobar_a']}], 'tests': [{'id': 'foobar_a'}], 'id': 'foobar_a'}
        sidefile_a.write_text(json.dumps(orig_test_project_a))

        sidefile_b = tmp_path / "b.json"
        orig_test_project_b = {'suites': [{'tests': ['foobar_b']}], 'tests': [{'id': 'foobar_b'}], 'id': 'foobar_b'}
        sidefile_b.write_text(json.dumps(orig_test_project_b))

        side_manager = SIDEProjectManager()
        project_id_a = side_manager.add_project(str(sidefile_a), None)
        test_project_a, test_suites_a, tests_a = side_manager.get_project(project_id_a)
        project_id_b = side_manager.add_project(str(sidefile_b), None)
        test_project_b, test_suites_b, tests_b = side_manager.get_project(project_id_b)

        assert project_id_a == 'foobar_a'
        assert project_id_b == 'foobar_b'
        assert test_project_a == orig_test_project_a
        assert test_suites_a == orig_test_project_a['suites']
        assert tests_a == {'foobar_a': {'id': 'foobar_a'}}
        assert tests_b == {'foobar_a': {'id': 'foobar_a'}, 'foobar_b': {'id': 'foobar_b'}}

    def test_parse_yaml_side_file(self, mocker):
        mocker.patch('side_runner_py.side.open')
        mocker.patch('json.load').side_effect = Exception()
        mocker.patch('yaml.safe_load').return_value = {}

        tests = []
        side_manager = SIDEProjectManager()
        side_manager._attach_params('foobar.yml', tests)
        assert tests == []
