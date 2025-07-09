from selenium.webdriver.ie.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from niffler_tests.configuration.ConfigProvider import ConfigProvider


class HeaderPage:

    __driver: WebDriver
    __timeout: float

    def __init__(self, driver: WebDriver, config: ConfigProvider):
        self.__driver = driver
        self.__timeout = config.get_timeout()

    def click_menu_button(self) -> None:
        self.__driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Menu"]').click()

    def click_profile(self) -> None:
        self.__driver.find_element(By.CSS_SELECTOR, 'a[class="link nav-link"]').click()

    def click_new_spending(self) -> None:

        WebDriverWait(self.__driver, self.__timeout).until(
            EC.visibility_of_element_located((
                By.CSS_SELECTOR, 'a[href="/spending"]'
            ))
        )
        self.__driver.find_element(By.CSS_SELECTOR, 'a[href="/spending"]').click()
