import os.path
import json
import pathlib
import traceback
import datetime
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


def execute_test(driver, test_project, test_suite, test_dict):
    try:
        handler_func = TEST_HANDLER_MAP[test_dict['command']]
        handler_func(driver, test_project, test_suite, test_dict)
    except Exception:
        traceback_msg = traceback.format_exc()
        logger.warning(traceback_msg)
        return True, traceback_msg
    return False, ""


def _ensure_test_suite_output(output, test_suite_id, create):
    f = [elm for elm in output if elm['id'] == test_suite_id]
    if f:
        return f[0]

    # create if not found test_suite output element
    output.append(create)
    return create


def _ensure_tests_output(output, tests_id, create):
    f = [elm for elm in output if elm['id'] == tests_id]
    if f:
        return f[0]

    # create if not found tests output element
    output.append(create)
    return create


def _call_hook_script(pattern):
    for filename in pathlib.Path(Config.HOOK_SCRIPTS_DIR).glob(pattern):
        if filename.exists():
            with filename.open() as f:
                logger.info('Call hookscript {}'. format(filename))
                exec(f.read())


def _execute_side_file(driver, side_manager, project_id):
    execute_datetime = datetime.datetime.now().replace(microsecond=0).isoformat().replace(':', '-').replace('T', '.')

    # prepare output directory
    outdir = pathlib.Path(Config.OUTPUT_DIR) / execute_datetime
    outdir.mkdir(parents=True, exist_ok=True)

    # start test
    output = []
    _call_hook_script('pre*.py')
    for test_project, test_suite, tests, idx, test in side_manager.get_tests_iter(project_id):
        logger.info('TEST: {}.{}.{}.{} to {} with {}'.format(
            test_suite['name'], tests['name'], idx, test['command'], test['target'], test['value']))
        get_screenshot(driver, test_suite['name'], tests['name'], idx, test, outdir)
        is_failed, failed_msg = execute_test(driver, test_project, test_suite, test)
        time.sleep(Config.DRIVER_COMMAND_WAIT / 1000)

        # generate test result
        test_command_output = {
            'comment': test.get('comment'),
            'command': test['command'],
            'target': test['target'],
            'value': test['value'],
            'is_failed': is_failed,
            'failed_msg': failed_msg
        }
        # ensure and get output dict referenct
        test_suite_output = _ensure_test_suite_output(
            output, test_suite['id'], {'name': test_suite['name'], 'tests': [], 'id': test_suite['id']})
        tests_output = _ensure_tests_output(
            test_suite_output['tests'], tests['id'], {'name': tests['name'], 'commands': [], 'id': tests['id']})
        # store test-command output
        tests_output['commands'].append(test_command_output)

        if is_failed:
            get_screenshot(driver, test_suite['name'], tests['name'], idx, test, outdir)

    # output test result
    with open(outdir / 'result.json', 'w') as f:
        json.dump(output, f, indent=4)


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

    # prepare webdriver
    driver = with_retry(Config.DRIVER_RETRY_COUNT, Config.DRIVER_RETRY_WAIT, initialize, Config.WEBDRIVER_URL)

    side_manager = SIDEProjectManager()
    for side_filename, param_filename in _get_side_file_list_by_glob(Config.SIDE_FILE):
        project_id = side_manager.add_project(side_filename, param_filename)
        _execute_side_file(driver, side_manager, project_id)


if __name__ == '__main__':
    main()
