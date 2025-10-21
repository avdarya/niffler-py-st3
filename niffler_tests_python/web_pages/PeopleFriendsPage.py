from urllib.parse import urljoin

from playwright.sync_api import Page, expect, Locator
from selenium.common import NoSuchElementException

from niffler_tests_python.settings.server_config import ServerConfig
from niffler_tests_python.web_pages.BasePage import BasePage
from niffler_tests_python.web_pages.components.NotificationComponent import NotificationComponent
from niffler_tests_python.web_pages.locators.PeopleFriendsPageLocators import PeopleFriendsPageLocators


class PeopleFriendsPage(BasePage):

    __url: str

    def __init__(self, page: Page,  server_cfg: ServerConfig):
        super().__init__(page, server_cfg)
        self.locators = PeopleFriendsPageLocators
        self.notification = NotificationComponent(page, server_cfg)
        self.__url = urljoin(str(server_cfg.frontend_url), '/people/friends')

    def get_friend_row(self, name: str) -> Locator | None:
        try:
            img_lonely_niffler = self.locators.img_lonely_niffler(self._page)
            if img_lonely_niffler.is_visible():
                return None
        except NoSuchElementException:
            pass
        while True:
            row = self.locators.friend_row(self._page, name)
            if row.count() > 0:
                row.wait_for(state="visible", timeout=3000)
                return row

            if self.locators.next_button(self._page).get_attribute('disabled') is not None:
                return None

            first_row = self._page.locator('tbody tr').first
            first_text = first_row.text_content()
            self.click_next_button()
            first_row.wait_for(state="visible")
            expect(first_row).not_to_have_text(first_text, timeout=5000)

    def click_accept(self, friend_row: Locator) -> None:
        self.locators.accept_button(friend_row).click()

    def click_decline(self, friend_row: Locator) -> None:
        self.locators.decline_button(friend_row).click()

    def click_unfriend(self, friend_row: Locator) -> None:
        self.locators.unfriend_button(friend_row).click()

    def click_next_button(self) -> None:
        self.locators.next_button(self._page).click()

    def click_popup_decline_button(self) -> None:
        self.locators.popup_decline_button(self._page).click()

    def click_popup_delete_button(self) -> None:
        self.locators.popup_delete_button(self._page).click()

    def expected_unfriend_button(self, friend_row: Locator) -> None:
        unfriend_btn = self.locators.unfriend_button(friend_row)
        expect(unfriend_btn).to_be_visible()
        expect(unfriend_btn).to_be_enabled()

    def get_all_usernames(self) -> list[str]:
        friend_rows = self.locators.friend_rows(self._page)
        friend_usernames = [self.locators.username_in_row(row) for row in friend_rows]
        return friend_usernames
