import time
from .config import Config
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoAlertPresentException
from logging import getLogger
logger = getLogger(__name__)


def execute_open(driver, test_project, test_suite, test_dict):
    # get url
    # FIXME: url try order impl (environment -> ttest[open].target -> test_suite.url -> test_project.url)
    base_url = test_project.get('url')
    driver.get(base_url + test_dict['target'])


def execute_set_window_size(driver, test_project, test_suite, test_dict):
    w, h = test_dict['target'].split('x')
    driver.set_window_size(w, h)


def execute_execute_script(driver, test_project, test_suite, test_dict):
    # FIXME: script argument support
    driver.execute_script(test_dict['target'])


# By.CLASS_NAME         By.ID                 By.NAME               By.TAG_NAME           By.mro(
# By.CSS_SELECTOR       By.LINK_TEXT          By.PARTIAL_LINK_TEXT  By.XPATH
def _get_element_selector_tuple(target_text):
    # FIXME: impl other selector
    text = target_text.split('=', 1)[1]
    if target_text.startswith('id='):
        return (By.ID, text)
    if target_text.startswith('xpath='):
        return (By.XPATH, text)
    if target_text.startswith('linkText='):
        return (By.LINK_TEXT, text)
    if target_text.startswith('css='):
        return (By.CSS_SELECTOR, text)
    if target_text.startswith('name='):
        return (By.NAME, text)


def _wait_element(driver, target_text):
    selector = _get_element_selector_tuple(target_text)
    logger.debug("click selector:", selector)
    condition = expected_conditions.presence_of_element_located(selector)
    element = WebDriverWait(driver, Config.DRIVER_ELEMENT_WAIT).until(condition)
    return element


def execute_click(driver, test_project, test_suite, test_dict):
    logger.debug("CLICK:", test_dict)
    element = _wait_element(driver, test_dict['target'])
    ActionChains(driver).click(element).perform()
    logger.debug("element:", element)


def execute_click_at(driver, test_project, test_suite, test_dict):
    logger.debug("CLICK AT:", test_dict)
    try:
        offsetx, offsety = ([int(s.strip()) for s in test_dict['value'].split(',')])
    except Exception:
        raise Exception('execute_click_at: illegal coord string: {}'.format(test_dict['value']))
    element = _wait_element(driver, test_dict['target'])
    ActionChains(driver).move_to_element_with_offset(element, offsetx, offsety).click(None).perform()
    logger.debug("element:", element)


def execute_double_click(driver, test_project, test_suite, test_dict):
    logger.debug("DOUBLE CLICK:", test_dict)
    element = _wait_element(driver, test_dict['target'])
    ActionChains(driver).double_click(element).perform()
    logger.debug("element:", element)


def execute_type(driver, test_project, test_suite, test_dict):
    logger.debug("TYPE:", test_dict)
    element = _wait_element(driver, test_dict['target'])

    # check target input element is or not date type
    # NOTE: send_keys on date-input is corrupted on webdriver (maybe)
    if element.get_attribute("type") == "date":
        (_, element_id) = _get_element_selector_tuple(test_dict['target'])
        script = "document.getElementById('{}').value = '{}';".format(element_id, test_dict['value'])
        driver.execute_script(script)
        return

    # element.send_keys(test_dict['value'])
    # ActionChains(driver).click(element).send_keys_to_element(element, test_dict['value']).perform()
    element.clear()
    ActionChains(driver).send_keys_to_element(element, test_dict['value']).perform()


def execute_pause(driver, test_project, test_suite, test_dict):
    logger.debug("PAUSE:", test_dict['target'], "[ms]")
    time.sleep(float(test_dict['target']) / 1000)


def execute_mouse_over(driver, test_project, test_suite, test_dict):
    element = _wait_element(driver, test_dict['target'])
    ActionChains(driver).move_to_element(element).perform()


def _select_by_selector(select, selector):
    text = selector.split('=', 1)[1]
    if selector.startswith('label='):
        return select.select_by_visible_text(text)


def execute_select(driver, test_project, test_suite, test_dict):
    element = _wait_element(driver, test_dict['target'])
    _select_by_selector(Select(element), test_dict['value'])


def execute_assert_confirmation(driver, test_project, test_suite, test_dict):
    expect = test_dict['target']
    elapsed_seconds = 0

    while True:
        try:
            actual = Alert(driver).text
            if expect in actual:
                return True
            else:
                raise Exception('execute_assert_confirmation: expected {}, actual {}'.format(expect, actual))
        except NoAlertPresentException:
            # FIXME: make configurable
            time.sleep(1)
            elapsed_seconds += 1
            if elapsed_seconds > Config.DRIVER_ELEMENT_WAIT:
                raise Exception('execute_assert_confirmation: expected {}, timed out'.format(expect))
            else:
                continue


def execute_webdriver_choose_ok_on_visible_confirmation(driver, test_project, test_suite, test_dict):
    Alert(driver).accept()


def execute_verify_text(driver, test_project, test_suite, test_dict):
    # FIXME: imple verify (get text and assert)
    _wait_element(driver, test_dict['target'])


TEST_HANDLER_MAP = {
    'open': execute_open,
    'setWindowSize': execute_set_window_size,
    'executeScript': execute_execute_script,
    'click': execute_click,
    'clickAt': execute_click_at,
    'doubleClick': execute_double_click,
    'type': execute_type,
    'pause': execute_pause,
    'verifyText': execute_verify_text,
    'mouseOver': execute_mouse_over,
    'select': execute_select,
    'mouseDownAt': lambda _1, _2, _3, _4: None,
    'mouseUpAt': lambda _1, _2, _3, _4: None,
    'mouseMoveAt': lambda _1, _2, _3, _4: None,
    'chooseOkOnNextConfirmation': lambda _1, _2, _3, _4: None,
    'chooseCancelOnNextConfirmation': lambda _1, _2, _3, _4: None,
    'assertConfirmation': execute_assert_confirmation,
    'webdriverChooseOkOnVisibleConfirmation': execute_webdriver_choose_ok_on_visible_confirmation,
}
