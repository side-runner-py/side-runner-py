import sys
import json


def print_result(suite_name, test_name, is_failed, use_emoji):
    if use_emoji:
        from emoji import emojize
        result_emoji = ":x:" if is_failed else ":o:"
        result_mark = emojize(result_emoji, use_aliases=True)
    else:
        result_mark = "x" if is_failed else "o"

    print("{0} {1} : {2}".format(suite_name, test_name, result_mark))


def is_expected(command):
    if 'expect failure' in command['comment']:
        return command['is_failed'] is True
    else:
        return command['is_failed'] is False


def run(result_file, use_emoji):
    with open(sys.argv[1]) as f:
        result = json.load(f)

    results = []
    for suite in result:
        suite["name"]
        for test in suite["tests"]:
            unexpected = any([not is_expected(c) for c in test["commands"]])
            print_result(suite["name"], test["name"], unexpected, use_emoji)
            results.append(unexpected)

    if any(results):
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("too few arguments")
        sys.exit(1)

    result_file = sys.argv[1]

    if len(sys.argv) >= 3 and sys.argv[2] == "--without-emoji":
        use_emoji = False
    else:
        use_emoji = True

    sys.exit(run(result_file, use_emoji))
