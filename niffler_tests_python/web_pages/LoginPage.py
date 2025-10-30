from playwright.sync_api import Page, expect

from urllib.parse import urljoin

from niffler_tests_python.settings.server_config import ServerConfig
from niffler_tests_python.web_pages.BasePage import BasePage
from niffler_tests_python.web_pages.locators.LoginPageLocators import LoginPageLocators


class LoginPage(BasePage):

    __url: str

    def __init__(self, page: Page, server_cfg: ServerConfig):
        super().__init__(page, server_cfg)
        self.__url = urljoin( str(server_cfg.auth_url),'/login')
        self.locators = LoginPageLocators

    def navigate(self):
        self._page.goto(self.__url)

    def expected_url(self):
        expect(self._page).to_have_url(self.__url)

    def fill_username(self, username: str) -> None:
        self.locators.username_input(self._page).type(username)

    def fill_password(self, password: str) -> None:
        self.locators.password_input(self._page).type(password)

    def submit(self) -> None:
        self.locators.submit_button(self._page).click()

    def click_create_new_account(self) -> None:
        self.locators.create_new_account_button(self._page).click()

    def is_correct_error_url(self):
        expect(self._page).to_have_url(f'{self.__url}?error')

    def is_visible_login_text(self):
        expect(self.locators.login_text(self._page)).to_be_visible()

    def is_visible_wrong_user_data_text(self):
        expect(self.locators.wrong_user_data_text(self._page)).to_be_visible(timeout=5000)
