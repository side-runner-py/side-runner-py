import os.path
import json
import time
import pathlib
import traceback
import datetime
import contextlib
from .commands import TEST_HANDLER_MAP
from .utils import with_retry
from .init import initialize
from .config import Config
from .side import SIDEProjectManager

from logging import basicConfig, INFO, getLogger
logger = getLogger(__name__)
basicConfig(level=INFO)


def get_screenshot(driver, test_suite_name, test_case_name, cmd_index, test_dict, outdir):
    from selenium.common.exceptions import UnexpectedAlertPresentException

    try:
        filename = "_".join([test_suite_name, test_case_name, "{0:02d}".format(cmd_index), test_dict['id']]) + ".png"
        driver.get_screenshot_as_file(os.path.join(outdir, filename))
    except UnexpectedAlertPresentException:
        logger.warning("Unable to get Screenshot due to alert present")
    except Exception:
        logger.warning(traceback.format_exc())


def _format_test_command_output(test, is_failed, failed_msg):
    # generate test result
    return {
        'comment': test.get('comment'),
        'command': test['command'],
        'target': test['target'],
        'value': test['value'],
        'is_failed': is_failed,
        'failed_msg': failed_msg
    }


def execute_test_command(driver, test_project, test_suite, test_dict):
    try:
        handler_func = TEST_HANDLER_MAP[test_dict['command']]
        handler_func(driver, test_project, test_suite, test_dict)
    except Exception:
        traceback_msg = traceback.format_exc()
        logger.warning(traceback_msg)
        return _format_test_command_output(test_dict, True, traceback_msg)
    return _format_test_command_output(test_dict, False, "")


def _ensure_test_output_by_id(output, some_id, create):
    f = [elm for elm in output if elm['id'] == some_id]
    if f:
        return f[0]

    # create if not found test_suite output element
    output.append(create)
    return create


def _store_test_command_output(output, test_suite, tests, test_command_output):
    # ensure and get output dict referenct
    test_suite_output = _ensure_test_output_by_id(
        output, test_suite['id'], {'name': test_suite['name'], 'tests': [], 'id': test_suite['id']})
    tests_output = _ensure_test_output_by_id(
        test_suite_output['tests'], tests['id'], {'name': tests['name'], 'commands': [], 'id': tests['id']})
    # store test-command output
    tests_output['commands'].append(test_command_output)


def _call_hook_script(pattern):
    for filename in pathlib.Path(Config.HOOK_SCRIPTS_DIR).glob(pattern):
        if filename.exists():
            with filename.open() as f:
                logger.info('Call hookscript {}'. format(filename))
                exec(f.read())


@contextlib.contextmanager
def _prepare_test_project_execution():
    # hold test execute time
    execute_datetime = datetime.datetime.now().replace(microsecond=0).isoformat().replace(':', '-').replace('T', '.')

    # prepare output directory
    outdir = pathlib.Path(Config.OUTPUT_DIR) / execute_datetime
    outdir.mkdir(parents=True, exist_ok=True)

    output = []
    try:
        _call_hook_script('pre*.py')

        # execute test
        yield output, outdir

        # FIXME: call post script
        # _call_hook_script('post*.py')

    finally:
        # output test result
        with open(outdir / 'result.json', 'w') as f:
            json.dump(output, f, indent=4)


def _generate_test_session(side_manager, project_id):
    test_project, test_suites, tests = side_manager.get_project(project_id)

    driver = None
    for test_suite in test_suites:
        for test_id in test_suite['tests']:
            for idx, test in enumerate(tests[test_id]['commands']):
                # prepare webdriver
                driver = with_retry(
                        Config.DRIVER_RETRY_COUNT, Config.DRIVER_RETRY_WAIT, initialize, Config.WEBDRIVER_URL)

                try:
                    yield driver, test_project, test_suite, tests[test_id], idx, test
                except Exception:
                    if driver:
                        driver.close()
                        driver = None

            if not test_suite.get('persistSessiona', False):
                if driver:
                    driver.close()
                    driver = None

        # close driver on test_suite execution finished
        if driver:
            driver.close()
            driver = None


def _execute_side_file(side_manager, project_id):
    with _prepare_test_project_execution() as (output, outdir):
        for driver, test_project, test_suite, tests, idx, test in _generate_test_session(side_manager, project_id):
            # log test-command
            test_path_str = '{}.{}.{}.{}'.format(test_suite['name'], tests['name'], idx, test['command'])
            logger.info('TEST: {} to {} with {}'.format(test_path_str, test['target'], test['value']))

            get_screenshot(driver, test_suite['name'], tests['name'], idx, test, outdir)

            # execute test command
            test_command_output = execute_test_command(driver, test_project, test_suite, test)
            _store_test_command_output(output, test_suite, tests, test_command_output)
            time.sleep(float(Config.DRIVER_COMMAND_WAIT) / 1000)

            if test_command_output['is_failed']:
                get_screenshot(driver, test_suite['name'], tests['name'], idx, test, outdir)
                raise Exception(test_command_output)


def _get_side_file_list_by_glob(pattern):
    # get SIDE file and param file absolute path pair
    base_dir = pathlib.Path(pattern).parent
    for side_filename in base_dir.glob(pathlib.Path(pattern).name):
        param_file_fullpath = base_dir / '{}_params.json'.format(side_filename.stem)
        side_file_fullpath = base_dir / side_filename
        if not param_file_fullpath.exists():
            yield (side_file_fullpath, None)
        else:
            yield (side_file_fullpath, param_file_fullpath)


def main():
    # load and evaluate config, env, defaults
    Config.init()

    # pre-load all tests
    side_manager = SIDEProjectManager()
    loaded_project_ids = [
        side_manager.add_project(side_filename, param_filename)
        for side_filename, param_filename in _get_side_file_list_by_glob(Config.SIDE_FILE)
    ]

    # execute test projects
    for project_id in loaded_project_ids:
        _execute_side_file(side_manager, project_id)


if __name__ == '__main__':
    main()
