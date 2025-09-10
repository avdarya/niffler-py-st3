from dataclasses import dataclass

from playwright.sync_api import Page, Locator


@dataclass(frozen=True)
class LoginPageLocators:

    @staticmethod
    def username_input(page: Page) -> Locator:
        return page.get_by_placeholder('Type your username')

    @staticmethod
    def password_input(page: Page) -> Locator:
        return page.get_by_placeholder('Type your password')

    @staticmethod
    def submit_button(page: Page) -> Locator:
        return page.get_by_role('button', name='Log in')

    @staticmethod
    def login_text(page: Page) -> Locator:
        return page.get_by_role('heading', name='Log in')

    @staticmethod
    def wrong_user_data_text(page: Page) -> Locator:
        return page.get_by_text('Неверные учетные данные пользователя')

    @staticmethod
    def create_new_account_button(page: Page) -> Locator:
        return page.get_by_role('link', name='Create new account')