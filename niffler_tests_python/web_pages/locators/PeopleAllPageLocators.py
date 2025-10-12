from dataclasses import dataclass

from playwright.sync_api import Page, Locator


@dataclass(frozen=True)
class PeopleAllPageLocators:

    @staticmethod
    def people_row(page: Page, name: str) -> Locator:
        return page.locator(f'//tr[contains(.,"{name}")]')

    @staticmethod
    def next_button(page: Page) -> Locator:
        return page.locator('#page-next')

    @staticmethod
    def add_friend_button(people_row: Locator) -> Locator:
        return people_row.get_by_role('button', name='Add friend')

    @staticmethod
    def waiting_chip(people_row: Locator) -> Locator:
        return people_row.get_by_text('Waiting...')

    @staticmethod
    def people_rows(page: Page) -> list[Locator]:
        return page.locator('tbody tr').all()

    @staticmethod
    def username_in_row(row: Locator) -> str:
        return row.locator('p').first.inner_text().strip()
