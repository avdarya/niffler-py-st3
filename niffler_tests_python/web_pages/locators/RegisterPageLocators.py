from dataclasses import dataclass

from playwright.sync_api import Page, Locator


@dataclass(frozen=True)
class RegisterPageLocators:

    @staticmethod
    def username_input(page: Page) -> Locator:
        return page.get_by_placeholder('Type your username')

    @staticmethod
    def password_input(page: Page) -> Locator:
        return page.get_by_placeholder('Type your password')

    @staticmethod
    def toggle_password_visibility(page: Page) -> Locator:
        return page.locator('#passwordBtn')

    @staticmethod
    def password_submit_input(page: Page) -> Locator:
        return page.get_by_placeholder('Submit your password')

    @staticmethod
    def submit_button(page: Page) -> Locator:
        return page.get_by_role('button', name='Sign Up')

    @staticmethod
    def success_message(page: Page) -> Locator:
        return page.get_by_text("Congratulations! You've registered!")

    @staticmethod
    def passwords_not_equal_message(page: Page) -> Locator:
        return page.get_by_text("Passwords should be equal")

    @staticmethod
    def success_signin_button(page: Page) -> Locator:
        return page.get_by_role('link', name='Sign in')

    @staticmethod
    def signup_text(page: Page) -> Locator:
        return page.get_by_role('heading', name='Sign up')
