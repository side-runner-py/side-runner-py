from pathlib import Path
from functools import partial
from importlib.machinery import SourceFileLoader
from .config import Config


def _any_or_match(curr_id_or_name, id_or_name):
    return id_or_name == '*' or id_or_name == curr_id_or_name


def _contains_id_or_name(conditions, kind, test_dict):
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


def run_per_project(pre_or_post, test_project):
    method_name = '{}_project_run'.format(pre_or_post)

    for hook_module in load_hook_scripts(Config.HOOK_SCRIPTS_DIR, '*.py'):
        conditions = getattr(hook_module, 'conditions', None)
        if conditions is None:
            continue

        if _contains_id_or_name(conditions, 'test_project', test_project):
            if getattr(hook_module, method_name, None):
                print('Call {}-project hookscript {}'. format(pre_or_post, hook_module.__name__))
                getattr(hook_module, method_name)()


def run_per_suite(pre_or_post, test_project, test_suite):
    method_name = '{}_suite_run'.format(pre_or_post)

    for hook_module in load_hook_scripts(Config.HOOK_SCRIPTS_DIR, '*.py'):
        conditions = getattr(hook_module, 'conditions', None)
        if conditions is None:
            continue

        if _contains_id_or_name(conditions, 'test_project', test_project) and \
           _contains_id_or_name(conditions, 'test_suite', test_suite):
            if getattr(hook_module, method_name, None):
                print('Call {}-suite hookscript {}'. format(pre_or_post, hook_module.__name__))
                getattr(hook_module, method_name)()


def run_per_test(pre_or_post, test_project, test_suite, test):
    method_name = '{}_test_run'.format(pre_or_post)

    for hook_module in load_hook_scripts(Config.HOOK_SCRIPTS_DIR, '*.py'):
        conditions = getattr(hook_module, 'conditions', None)
        if conditions is None:
            continue

        if _contains_id_or_name(conditions, 'test_project', test_project) and \
           _contains_id_or_name(conditions, 'test_suite', test_suite) and \
           _contains_id_or_name(conditions, 'test', test):
            if getattr(hook_module, method_name, None):
                print('Call {}-test hookscript {}'. format(pre_or_post, hook_module.__name__))
                getattr(hook_module, method_name)()
