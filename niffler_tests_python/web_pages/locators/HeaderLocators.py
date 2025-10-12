from dataclasses import dataclass
from selenium.webdriver.common.by import By
from dataclasses import dataclass

from playwright.sync_api import Page, Locator


@dataclass(frozen=True)
class HeaderLocators:
    # MENU_BUTTON = (By.CSS_SELECTOR, 'button[aria-label="Menu"]')
    # PROFILE_BUTTON = (By.CSS_SELECTOR, 'a[href = "/profile"]')
    # SPENDING_BUTTON = (By.CSS_SELECTOR, 'a[href="/spending"]')
    # ACCOUNT_MENU= (By.ID, 'account-menu')

    @staticmethod
    def spending_button(page: Page) -> Locator:
        return page.get_by_role('link', name='New spending')

    @staticmethod
    def person_icon(page: Page) -> Locator:
        return page.get_by_test_id('PersonIcon')

    @staticmethod
    def profile_button(page: Page) -> Locator:
        return page.get_by_role('menuitem', name='Profile')

    @staticmethod
    def friends_button(page: Page) -> Locator:
        return page.get_by_role('menuitem', name='Friends')

    @staticmethod
    def all_people_button(page: Page) -> Locator:
        return page.get_by_role('menuitem', name='All people')