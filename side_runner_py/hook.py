from pathlib import Path
from functools import partial
from importlib.machinery import SourceFileLoader
from .config import Config
from .utils import call_with_argname_bind

from .log import getLogger
logger = getLogger(__name__)


def _any_or_match(curr_id_or_name, id_or_name):
    return id_or_name == '*' or id_or_name == curr_id_or_name


def _contains_id_or_name(kind, test_dict, conditions):
    id = test_dict.get('id', '')
    name = test_dict.get('name', '')

    return \
        any(filter(partial(_any_or_match, id), conditions.get(kind + '_ids', []))) or \
        any(filter(partial(_any_or_match, name), conditions.get(kind + '_names', [])))


def load_hook_scripts(hook_script_dir, pattern):
    filename_list = list(Path(hook_script_dir).glob(pattern))
    filename_list.sort()
    for filename in filename_list:
        if filename.exists():
            loader = SourceFileLoader(str(filename.parent / filename.stem), str(filename))
            yield loader.load_module()


def _run_hook(pre_or_post, kind, match_funcs, current_test_dict):
    method_name = '{}_{}_run'.format(pre_or_post, kind)

    for hook_module in load_hook_scripts(Config.HOOK_SCRIPTS_DIR, '*.py'):
        conditions = getattr(hook_module, 'conditions', None)
        if conditions is None:
            continue

        if all([f(conditions) for f in match_funcs]):
            if getattr(hook_module, method_name, None):
                logger.info('Call {}-{} hookscript {}.py'.format(pre_or_post, kind, hook_module.__name__))
                func = getattr(hook_module, method_name)
                call_with_argname_bind(func, current_test_dict)


def run_hook_per_project(pre_or_post, test_project):
    kind = 'project'
    match_funcs = [
        partial(_contains_id_or_name, 'test_project', test_project),
    ]
    current_test_dict = {
        'test_project': test_project,
    }
    _run_hook(pre_or_post, kind, match_funcs, current_test_dict)


def run_hook_per_suite(pre_or_post, test_project, test_suite):
    kind = 'suite'
    match_funcs = [
        partial(_contains_id_or_name, 'test_project', test_project),
        partial(_contains_id_or_name, 'test_suite', test_suite),
    ]
    current_test_dict = {
        'test_project': test_project,
        'test_suite': test_suite,
    }
    _run_hook(pre_or_post, kind, match_funcs, current_test_dict)


def run_hook_per_test(pre_or_post, test_project, test_suite, test):
    kind = 'test'
    match_funcs = [
        partial(_contains_id_or_name, 'test_project', test_project),
        partial(_contains_id_or_name, 'test_suite', test_suite),
        partial(_contains_id_or_name, 'test', test),
    ]
    current_test_dict = {
        'test_project': test_project,
        'test_suite': test_suite,
        'test': test,
    }
    _run_hook(pre_or_post, kind, match_funcs, current_test_dict)
