from dataclasses import dataclass

from playwright.sync_api import Page, Locator


@dataclass(frozen=True)
class HeaderLocators:

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