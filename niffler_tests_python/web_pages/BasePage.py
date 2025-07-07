from selenium.webdriver.ie.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from niffler_tests_python.configuration.ConfigProvider import ConfigProvider


class BasePage:

    _drive: WebDriver
    _timeout: float

    def __init__(self, driver: WebDriver, config: ConfigProvider):
        self._driver = driver
        self._timeout = config.get_timeout()


    def wait_for_visibility_element(self, locator: tuple[str, str]) -> WebElement:
        return WebDriverWait(self._driver, self._timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_for_visibility_elements(self, locator: tuple[str, str]) -> list[WebElement]:
        return WebDriverWait(self._driver, self._timeout).until(
            EC.visibility_of_any_elements_located(locator)
        )

    def wait_for_presence_element(self, locator: tuple[str, str]) -> WebElement:
        return  WebDriverWait(self._driver, self._timeout).until(
            EC.presence_of_element_located(locator)
        )