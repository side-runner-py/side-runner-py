conditions = {
    'test_project_ids': ['*'],
    'test_suite_ids': ['*'],
    'test_ids': ['*'],
}


def pre_project_run():
    print('Test Project pre-script.')


def post_project_run():
    print('Test Project post-script.')


def pre_suite_run():
    print('Test Suite pre-script.')


def post_suite_run():
    print('Test Suite post-script.')


def pre_test_run():
    print('Test pre-script.')


def post_test_run():
    print('Test post-script.')
