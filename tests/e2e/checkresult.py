import sys
import json
from emoji import emojize


def print_result(suite_name, test_name, is_failed):
    result_emoji = ":x:" if is_failed else ":o:"
    print("{0} {1} : {2}".format(suite_name, test_name, emojize(result_emoji, use_aliases=True)))


with open(sys.argv[1]) as f:
    result = json.load(f)


results = []
for suite in result:
    suite["name"]
    for test in suite["tests"]:
        is_failed = any([c["is_failed"] for c in test["commands"]])
        print_result(suite["name"], test["name"], is_failed)
        results.append(is_failed)


if any(results):
    sys.exit(1)
else:
    sys.exit(0)
