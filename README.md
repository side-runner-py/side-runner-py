[![Build Status](https://travis-ci.org/side-runner-py/side-runner-py.svg?branch=master)](https://travis-ci.org/side-runner-py/side-runner-py)
[![codecov](https://codecov.io/gh/side-runner-py/side-runner-py/branch/master/graph/badge.svg)](https://codecov.io/gh/side-runner-py/side-runner-py)

## Getting started

```
pip install git+https://github.com/side-runner-py/side-runner-py.git
side-runner-py -h
```

## Settings
| Command-line argument       | Environment paramter      | Default                        | Description                                       |
| --------------------------- | ------------------------- | ------------------------------ | ------------------------------------------------- |
| --webdriver-url             | SIDE_WEBDRIVER_URL        | 'http://webdriver:4444/wd/hub' | URL of Selenium WebDriver                         |
| --test-file                 | SIDE_TEST_FILE            | default.side                   | Selenium IDE "SIDE" file-path pattern for testing |
| --http-proxy                | HTTP_PROXY                | ''                             | Proxy settings within WebDriver                   |
| --https-proxy               | HTTPS_PROXY               | ''                             | Proxy settings within WebDriver                   |
| --no-proxy                  | NO_PROXY                  | ''                             | Proxy settings within WebDriver                   |
| --output-dir                | SIDE_OUTPUT_DIR           | ./output                       | Test result output directory path                 |
| --desired-capabilities / -c | SIDE_DESIRED_CAPABILITIES | []                             | WebDriver's desired capabilities                  |
| --driver-retry-count        | SIDE_DRIVER_RETRY_COUNT   | 5                              | Driver initialize retry count                     |
| --driver-retry-wait         | SIDE_DRIVER_RETRY_WAIT    | 5 [sec]                        | Driver initialize wait time                       |
| --driver-element-wait       | SIDE_DRIVER_ELEMENT_WAIT  | 10 [sec]                       | Maximum wait time of element selection            |
| --driver-command-wait       | SIDE_DRIVER_COMMAND_WAIT  | 0 [ms]                         | Wait time between test commands                   |
| --hook-scripts-dir          | SIDE_HOOK_SCRIPTS_DIR     | 'hooks'                        | Pre hook python script directory                  |
| --log-level                 | SIDE_LOG_LEVEL            | 'INFO'                         | Log level of 'logging' library                    |

## How to use hook
1. Make a hook directory.
2. Store hook script files into the hook directory.
  - the script file name must be `*.py`.
3. Implement the hook script.
  - put a module global variable `conditions`.
    - it's type of `dict`.
    - it has some filters.
      - the key name format is `test[_project|_suite|]_[ids|names]`. (e.g. `test_project_ids`,`test_suite_ids`,`test_names`)
      - the value is a list of id or name.
      - or, `test_command_[ids|types|indexes]`. (e.g. `test_command_types`,`test_command_indexes`)
      - you can use the all match(`'*'`) instead of id or name but can not use glob pattern.
  - write some functions.
    - the function name format is `[pre|post]_[project|suite|test|command]_run`. (e.g. `pre_suite_run`,`post_test_run`,`post_command_run`)
    - the function may have arguments named `test_project`,`test_suite`,`test`,`test_command`.
      - they have current test details.
      - they are just objects in `.side` file.
      - the other objects are not passed except above.
    - the function may have arguments named `test_command_index`.
    - the function may have arguments named `session_manager`.
      - it's has Remove Webdriver named `driver`.
4. Specify the hook directory as the argument of `--hook-scripts-dir`.
