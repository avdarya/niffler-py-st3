from typing import Tuple, Callable
from selenium.webdriver.ie.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from niffler_tests_python.configuration.ConfigProvider import ConfigProvider

Locator = Tuple[str, str]
Condition = Callable[[Locator], Callable[[WebDriver], object]]

class BasePage:

    _driver: WebDriver
    _timeout: float
    _poll: float

    def __init__(self, driver: WebDriver, config: ConfigProvider):
        self._driver = driver
        self._timeout = config.get_timeout()
        self._poll = config.get_poll()

    def wait_for(
            self,
            locator: Locator,
            condition: Condition = EC.presence_of_element_located,
            timeout: float | None = None,
            poll: float | None = None
    ):
        return WebDriverWait(
            driver = self._driver,
            timeout= timeout or self._timeout,
            poll_frequency= poll or self._poll
        ).until(condition(locator))

    def wait_for_staleness(
            self,
            element: WebElement,
            timeout: float | None = None,
            poll: float | None = None
    ) -> bool:
        return WebDriverWait(
            driver = self._driver,
            timeout=timeout or self._timeout,
            poll_frequency=poll or self._poll
        ).until(EC.staleness_of(element))