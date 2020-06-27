import sys
import json

conditions = {
    'test_project_ids': ['*'],
    'test_suite_ids': ['*'],
    'test_ids': ['*'],
    'test_command_types': ['click'],
}


def _log(pre_post, session_manager, test, test_command, test_command_index):
    with open("/hook-logs/log.txt", "a") as f:
        msg_dict = {
            "session_id": session_manager.driver.session_id,
            "test_name": test["name"],
            "command": test_command["command"],
            "command_index": test_command_index,
        }
        for out in [f, sys.stdout]:
            print("{}_command_hook: {}".format(pre_post, json.dumps(msg_dict)), file=out, flush=True)


def pre_command_run(session_manager, test, test_command, test_command_index):
    _log("pre", session_manager, test, test_command, test_command_index)


def post_command_run(session_manager, test, test_command, test_command_index):
    _log("post", session_manager, test, test_command, test_command_index)
