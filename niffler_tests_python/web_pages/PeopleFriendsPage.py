import time
from urllib.parse import urljoin

from playwright.sync_api import Page, expect, Locator

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
        self._page.wait_for_timeout(1000)
        deadline = time.time() + 10000 / 1000
        direction = "next"

        while time.time() < deadline:
            try:
                if self.locators.img_lonely_niffler(self._page).is_visible():
                    return None
            except Exception:
                pass

            row = self.locators.friend_row(self._page, name)
            if row.count() > 0:
                row = row.first
                row.scroll_into_view_if_needed(timeout=2000)
                row.wait_for(state="visible", timeout=5000)
                return row

            first_row = self.locators.friend_rows_locator(self._page).first
            old_text = None
            try:
                if first_row.count() > 0:
                    old_text = first_row.text_content()
            except Exception:
                pass

            next_btn = self.locators.next_button(self._page)
            prev_btn = getattr(self.locators, "prev_button", None)
            moved = False

            if direction == "next" and next_btn.is_enabled():
                next_btn.click()
                moved = True
            elif prev_btn and prev_btn(self._page).is_enabled():
                prev_btn(self._page).click()
                moved = True
                direction = "prev"
            elif next_btn.is_enabled():
                next_btn.click()
                moved = True

            if moved:
                if old_text:
                    try:
                        expect(first_row).not_to_have_text(old_text, timeout=5000)
                    except Exception:
                        self._page.wait_for_timeout(250)
                else:
                    self._page.wait_for_timeout(250)
                continue

            self._page.wait_for_timeout(200)

        return None

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
        first_row = self.locators.friend_rows_locator(self._page).first
        expect(first_row).to_be_visible(timeout=5000)
        friend_rows = self.locators.friend_rows(self._page)
        friend_usernames = [self.locators.username_in_row(row) for row in friend_rows]
        return friend_usernames
