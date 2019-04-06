import json
import yaml
from copy import deepcopy
from itertools import product
from functools import reduce
from jinja2 import Environment


class SIDEProjectManager:
    def __init__(self):
        # store tests across test-project
        self.tests = {}
        # store test-project across test-project
        self.projects = {}

    def add_project(self, side_filename, param_filename):
        # load .side file
        test_project, test_suites, tests = self._parse_side(side_filename)

        # store to manager attributes
        self.tests.update(tests)
        self.projects[test_project['id']] = {
            'project': test_project,
            'tests': tests,
            'test_suites': test_suites,
            'param_filename': param_filename
        }

        return test_project['id']

    def get_project(self, project_id):
        test_project = self.projects[project_id]

        # deepcopy tests
        tests = deepcopy(test_project['tests'])
        test_suites = deepcopy(test_project['test_suites'])

        # expand parameters if param file exists
        if test_project['param_filename']:
            self._attach_params(test_project['param_filename'], tests)
            test_suites, tests = self._expand_test_project_with_params(test_suites, tests)

        # extend manager's tests and parameter expanded tests
        all_tests = deepcopy(self.tests)
        all_tests.update(tests)

        return test_project['project'], test_suites, all_tests

    def _parse_side(self, filename):
        # parse json
        test_project = {}
        with open(filename, 'r') as f:
            test_project = json.load(f)

        # load test suites
        test_suites = test_project['suites']

        # load tests
        tests = {}
        for test in test_project['tests']:
            tests[test['id']] = test

        return test_project, test_suites, tests

    def _attach_params(self, params_filename, tests):
        # parse json
        with open(params_filename, 'r') as f:
            test_params = json.load(f)

        # calc matrix param
        for test_param in test_params:
            if test_param['params_type'] == 'matrix':
                test_param['params'] = _dict_product(test_param['params'])

        # get test ID by test name
        for test_param in test_params:
            test_param['test_id'] = _get_test_id(tests, test_param['test_name'])

        # attach to tests
        for test_param in test_params:
            tests[test_param['test_id']]['params'] = test_param['params']

    def _expand_tests_with_params(self, tests):
        # expand test
        new_tests = {}
        expanded_test_original_ids = []

        # filter tests with params attched or not
        params_attached_tests = [test for test in tests.values() if 'params' in test]

        for test in params_attached_tests:
            expanded_test_original_ids.append(test['id'])
            for idx, param in enumerate(test['params']):
                new_id = '{0}-{1}'.format(test['id'], idx)
                new_tests[new_id] = _render_param(test, param)
                new_tests[new_id]['id'] = new_id
                new_tests[new_id]['name'] = '{0}-{1}'.format(test['name'], idx)
        return new_tests, expanded_test_original_ids

    def _expand_test_suites_with_params(self, test_suites, tests, expanded_tests):
        # expand test suite
        new_suites = []
        expanded_suites = []
        for idx, test_suite in enumerate(test_suites):
            # filter parameter expanded test-dict
            contains_tests = [tests[test_id] for test_id in expanded_tests if test_id in test_suite['tests']]
            if len(contains_tests) == 0:
                continue
            expanded_suites.append(idx)

            for id_idx_tuples in product(*[[(t['id'], idx)
                                         for idx in range(len(t['params']))] for t in contains_tests]):
                suite_idx = '-'.join([str(idx) for _, idx in id_idx_tuples])
                new_id = '{0}-{1}'.format(test_suite['id'], suite_idx)

                new_suite = deepcopy(test_suite)
                new_suite['id'] = new_id
                new_suite['name'] = '{0}-{1}'.format(test_suite['name'], suite_idx)
                for test_id, idx in id_idx_tuples:
                    new_suite['tests'] = ['{0}-{1}'.format(oldid, idx)
                                          if oldid == test_id else oldid for oldid in new_suite['tests']]

                new_suites.append(new_suite)
        return new_suites, expanded_suites

    def _expand_test_project_with_params(self, test_suites, tests):
        new_tests, expanded_tests = self._expand_tests_with_params(tests)
        new_suites, expanded_suites = self._expand_test_suites_with_params(test_suites, tests, expanded_tests)

        # update objects
        tests.update(new_tests)
        test_suites.extend(new_suites)

        # remove original test
        for test_id in expanded_tests:
            tests.pop(test_id)

        # remove original test suite
        test_suites = [suite for idx, suite in enumerate(test_suites) if idx not in expanded_suites]

        return test_suites, tests


def _get_test_id(tests, test_name):
    return [test['id'] for test in tests.values() if test['name'] == test_name][0]


def _render_param(test, param):
    env = Environment(variable_start_string='{$', variable_end_string='$}')
    return json.loads(env.from_string(json.dumps(test)).render(param))


def _dict_product(d):
    """Return Cartesian product of arrays of dictionary

    >>> _dict_product({"a": [1,2], "b": [10,20]})
    [{'a': 1, 'b': 10}, {'a': 1, 'b': 20}, {'a': 2, 'b': 10}, {'a': 2, 'b': 20}]
    """
    def _combine(acc, val):
        acc.update(val)
        return acc

    return [reduce(_combine, item, {}) for item in product(*[[{k: v} for v in arr] for k, arr in d.items()])]


if __name__ == '__main__':
    import doctest
    doctest.testmod()
