import sys
import json

conditions = {
    'test_project_ids': ['*'],
    'test_suite_ids': ['*'],
    'test_ids': ['*'],
}


def _log(pre_post, test):
    with open("/hook-logs/log.txt", "a") as f:
        msg_dict = {"test_name": test["name"]}
        for out in [f, sys.stdout]:
            print("{}_test_hook: {}".format(pre_post, json.dumps(msg_dict)), file=out, flush=True)


def pre_test_run(test):
    _log("pre", test)


def post_test_run(test):
    _log("post", test)
