import allure

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.webdriver import WebDriver
from urllib.parse import urljoin

from niffler_tests_python.settings.server_config import ServerConfig
from niffler_tests_python.web_pages.BasePage import BasePage
from niffler_tests_python.web_pages.locators.LoginPageLocators import LoginPageLocators


class LoginPage(BasePage):

    __url: str

    def __init__(self, driver: WebDriver, server_cfg: ServerConfig):
        super().__init__(driver, server_cfg)
        self.__url = urljoin(str(server_cfg.frontend_url),'/login')
        self.locator = LoginPageLocators()

    @allure.step('[UI /login] Open /login')
    def open(self) -> None:
        self._driver.get(self.__url)

    @allure.step('[UI /login] Enter username: username={username}')
    def enter_username(self, username: str) -> None:
        self.wait_for(self.locator.USERNAME_INPUT, EC.visibility_of_element_located)
        self._driver.find_element(*self.locator.USERNAME_INPUT).send_keys(username)

    @allure.step('[UI /login] Enter password: password={password}')
    def enter_password(self, password: str) -> None:
        self._driver.find_element(*self.locator.PASSWORD_INPUT).send_keys(password)

    @allure.step('[UI /login] Click login button')
    def click_login_button(self) -> None:
        self._driver.find_element(*self.locator.SUBMIT_BUTTON).click()
        self.wait_for(self.locator.NIFFLER_LOGO)
