import sys
import json
from emoji import emojize


def print_result(suite_name, test_name, is_failed):
    result_emoji = ":x:" if is_failed else ":o:"
    print("{0} {1} : {2}".format(suite_name, test_name, emojize(result_emoji, use_aliases=True)))


def is_expected(command):
    if 'expect failure' in command['comment']:
        return command['is_failed'] is True
    else:
        return command['is_failed'] is False


with open(sys.argv[1]) as f:
    result = json.load(f)

results = []
for suite in result:
    suite["name"]
    for test in suite["tests"]:
        unexpected = any([not is_expected(c) for c in test["commands"]])
        print_result(suite["name"], test["name"], unexpected)
        results.append(unexpected)


if any(results):
    sys.exit(1)
else:
    sys.exit(0)
