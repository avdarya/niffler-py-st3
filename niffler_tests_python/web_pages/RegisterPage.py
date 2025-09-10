from urllib.parse import urljoin

from playwright.sync_api import Page, expect

from niffler_tests_python.settings.server_config import ServerConfig
from niffler_tests_python.web_pages.BasePage import BasePage
from niffler_tests_python.web_pages.locators.RegisterPageLocators import RegisterPageLocators

class RegisterPage(BasePage):

    __url: str

    def __init__(self, page: Page, server_config: ServerConfig) -> None:
        super().__init__(page, server_config)
        self.locators = RegisterPageLocators
        self.__url = urljoin(str(server_config.auth_url),'/register')

    def navigate(self):
        self._page.goto(self.__url)

    def fill_username(self, username: str) -> None:
        self.locators.username_input(self._page).type(username)

    def fill_password(self, password: str) -> None:
        self.locators.password_input(self._page).type(password)

    def fill_password_submit(self, password: str) -> None:
        self.locators.password_submit_input(self._page).type(password)

    def submit(self) -> None:
        self.locators.submit_button(self._page).click()

    def click_success_signin(self) -> None:
        self.locators.success_signin_button(self._page).click()

    def toggle_password_visibility(self) -> None:
        self.locators.toggle_password_visibility(self._page).click()

    def is_correct_url(self):
        expect(self._page).to_have_url(self.__url)

    def expect_password_hidden(self) -> None:
        expect(self.locators.password_input(self._page)).to_have_attribute('type', 'password')

    def expect_password_visible(self) -> None:
        expect(self.locators.password_input(self._page)).to_have_attribute('type', 'text')

    def is_show_success_message(self):
        expect(self.locators.success_message(self._page)).to_be_visible()

    def is_show_passwords_should_by_equal(self):
        expect(self.locators.passwords_not_equal_message(self._page)).to_be_visible()

    def is_show_success_signin_button(self):
        expect(self.locators.success_signin_button(self._page)).to_be_visible()

    def is_visible_signup_text(self):
        expect(self.locators.signup_text(self._page)).to_be_visible()
