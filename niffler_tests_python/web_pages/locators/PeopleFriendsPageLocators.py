from dataclasses import dataclass

from playwright.sync_api import Page, Locator


@dataclass(frozen=True)
class PeopleFriendsPageLocators:

    @staticmethod
    def friend_row(page: Page, name: str) -> Locator:
        return page.locator(f'//tr[contains(.,"{name}")]')

    @staticmethod
    def next_button(page: Page) -> Locator:
        return page.locator('#page-next')

    @staticmethod
    def accept_button(friend_row: Locator) -> Locator:
        return friend_row.get_by_role('button', name='Accept')

    @staticmethod
    def decline_button(friend_row: Locator) -> Locator:
        return friend_row.get_by_role('button', name='Decline')

    @staticmethod
    def unfriend_button(friend_row: Locator) -> Locator:
        return friend_row.get_by_role('button', name='Unfriend')

    @staticmethod
    def popup_decline_button(page: Page) -> Locator:
        return page.get_by_role("dialog").get_by_role("button", name="Decline")

    @staticmethod
    def popup_delete_button(page: Page) -> Locator:
        return page.get_by_role("dialog").get_by_role("button", name="Delete")

    @staticmethod
    def img_lonely_niffler(page: Page) -> Locator:
        return page.get_by_alt_text('Lonely niffler')

    @staticmethod
    def friend_rows(page: Page) -> list[Locator]:
        return page.locator('tbody tr').all()

    @staticmethod
    def username_in_row(row: Locator) -> str:
        return row.locator('p').first.inner_text().strip()
