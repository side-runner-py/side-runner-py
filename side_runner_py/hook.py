from pathlib import Path
from functools import partial
from importlib.machinery import SourceFileLoader
from .config import Config


def _any_or_match(curr_id_or_name, id_or_name):
    return id_or_name == '*' or id_or_name == curr_id_or_name


def _contains_id_or_name(kind, test_dict, conditions):
    id = test_dict.get('id', '')
    name = test_dict.get('name', '')

    return \
        any(filter(partial(_any_or_match, id), conditions.get(kind + '_ids', []))) or \
        any(filter(partial(_any_or_match, name), conditions.get(kind + '_names', [])))


def load_hook_scripts(hook_script_dir, pattern):
    for filename in Path(hook_script_dir).glob(pattern):
        if filename.exists():
            loader = SourceFileLoader(str(filename.parent / filename.stem), str(filename))
            yield loader.load_module()


def _run_hook(pre_or_post, kind, match_funcs):
    method_name = '{}_{}_run'.format(pre_or_post, kind)

    for hook_module in load_hook_scripts(Config.HOOK_SCRIPTS_DIR, '*.py'):
        conditions = getattr(hook_module, 'conditions', None)
        if conditions is None:
            continue

        if all([f(conditions) for f in match_funcs]):
            if getattr(hook_module, method_name, None):
                print('Call {}-{} hookscript {}'. format(pre_or_post, kind, hook_module.__name__))
                getattr(hook_module, method_name)()


def run_per_project(pre_or_post, test_project):
    kind = 'project'
    match_funcs = [
        partial(_contains_id_or_name, 'test_project', test_project),
    ]
    _run_hook(pre_or_post, kind, match_funcs)


def run_per_suite(pre_or_post, test_project, test_suite):
    kind = 'suite'
    match_funcs = [
        partial(_contains_id_or_name, 'test_project', test_project),
        partial(_contains_id_or_name, 'test_suite', test_suite),
    ]
    _run_hook(pre_or_post, kind, match_funcs)


def run_per_test(pre_or_post, test_project, test_suite, test):
    kind = 'test'
    match_funcs = [
        partial(_contains_id_or_name, 'test_project', test_project),
        partial(_contains_id_or_name, 'test_suite', test_suite),
        partial(_contains_id_or_name, 'test', test),
    ]
    _run_hook(pre_or_post, kind, match_funcs)
