[![Build Status](https://travis-ci.org/side-runner-py/side-runner-py.svg?branch=master)](https://travis-ci.org/side-runner-py/side-runner-py)
[![codecov](https://codecov.io/gh/side-runner-py/side-runner-py/branch/master/graph/badge.svg)](https://codecov.io/gh/side-runner-py/side-runner-py)

## Getting started

```
pip install git+https://github.com/side-runner-py/side-runner-py.git
side-runner-py -h
```

## Settings
| Command-line argument | Environment paramter      | Default                        | Description                                       |
| --------------------- | ------------------------- | ------------------------------ | ------------------------------------------------- |
| --webdriver-url       | SIDE_WEBDRIVER_URL        | 'http://webdriver:4444/wd/hub' | URL of Selenium WebDriver                         |
| --test-file           | SIDE_TEST_FILE            | default.side                   | Selenium IDE "SIDE" file-path pattern for testing |
| --http-proxy          | HTTP_PROXY                | ''                             | Proxy settings within WebDriver                   |
| --https-proxy         | HTTPS_PROXY               | ''                             | Proxy settings within WebDriver                   |
| --no-proxy            | NO_PROXY                  | ''                             | Proxy settings within WebDriver                   |
| --output-dir          | SIDE_OUTPUT_DIR           | ./output                       | Test result output directory path                 |
| --driver-retry-count  | SIDE_DRIVER_RETRY_COUNT   | 5                              | Driver initialize retry count                     |
| --driver-retry-wait   | SIDE_DRIVER_RETRY_WAIT    | 5 [sec]                        | Driver initialize wait time                       |
| --driver-element-wait | SIDE_DRIVER_ELEMENT_WAIT  | 10 [sec]                       | Maximum wait time of element selection            |
| --driver-command-wait | SIDE_DRIVER_COMMAND_WAIT  | 0 [ms]                         | Wait time between test commands                   |
| --hook-scripts-dir    | SIDE_HOOK_SCRIPTS_DIR     | 'hooks'                        | Pre hook python script directory                  |
| --log-level           | SIDE_LOG_LEVEL            | 'INFO'                         | Log level of 'logging' library                    |
