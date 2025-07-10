import allure
from selenium.webdriver.ie.webdriver import WebDriver
from niffler_tests_python.configuration.ConfigProvider import ConfigProvider
from niffler_tests_python.web_pages.BasePage import BasePage
from niffler_tests_python.web_pages.locators.HeaderLocators import HeaderLocators


class Header(BasePage):

    def __init__(self, driver: WebDriver, config: ConfigProvider):
        super().__init__(driver, config)
        self.locator = HeaderLocators()

    @allure.step('[UI header]')
    def click_menu_button(self) -> None:
        self._driver.find_element(*self.locator.MENU_BUTTON).click()

    @allure.step('[UI header] Click profile button')
    def click_profile(self) -> None:
        self._driver.find_element(*self.locator.PROFILE_BUTTON).click()

    @allure.step('[UI header] Click new spending button')
    def click_new_spending(self) -> None:
        self._driver.find_element(*self.locator.SPENDING_BUTTON).click()
