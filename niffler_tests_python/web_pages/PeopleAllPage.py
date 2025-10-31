import time
from urllib.parse import urljoin

from playwright.sync_api import Page, expect, Locator

from niffler_tests_python.settings.server_config import ServerConfig
from niffler_tests_python.web_pages.BasePage import BasePage
from niffler_tests_python.web_pages.components.NotificationComponent import NotificationComponent
from niffler_tests_python.web_pages.locators.PeopleAllPageLocators import PeopleAllPageLocators


class PeopleAllPage(BasePage):

    __url: str

    def __init__(self, page: Page,  server_cfg: ServerConfig):
        super().__init__(page, server_cfg)
        self.locators = PeopleAllPageLocators
        self.notification = NotificationComponent(page, server_cfg)
        self.__url = urljoin(str(server_cfg.frontend_url), '/people/all')

    def get_people_row(self, name: str) -> Locator | None:
        self._page.wait_for_timeout(1000)
        timeout_ms = 10_000
        deadline = time.time() + timeout_ms / 1000

        while time.time() < deadline:
            row = self.locators.people_row(self._page, name)
            if row.count() > 0:
                row = row.first
                row.wait_for(state="visible", timeout=5000)
                return row

            next_btn = self.locators.next_button(self._page)
            if next_btn.is_enabled():
                first_row = self._page.locator('tbody tr').first
                old_text = None
                try:
                    if first_row.count() > 0:
                        old_text = first_row.text_content()
                except Exception:
                    pass

                next_btn.click()

                if old_text:
                    try:
                        expect(first_row).not_to_have_text(old_text, timeout=5000)
                    except Exception:
                        self._page.wait_for_timeout(300)
                else:
                    self._page.wait_for_timeout(300)
                continue

            prev_btn = getattr(self.locators, "prev_button", None)
            if prev_btn:
                prev = prev_btn(self._page)
                if prev.is_enabled():
                    prev.click()
                    self._page.wait_for_timeout(200)
                    continue

            self._page.wait_for_timeout(250)

        return None

    def click_add_friend(self, people_row: Locator) -> None:
        self.locators.add_friend_button(people_row).click()

    def click_next_button(self) -> None:
        self.locators.next_button(self._page).click()

    def expected_waiting_chip(self, people_row: Locator) -> None:
        expect(self.locators.waiting_chip(people_row)).to_be_visible()

    def get_all_usernames(self) -> list[str]:
        people_rows = self.locators.people_rows(self._page)
        people_usernames = [self.locators.username_in_row(row) for row in people_rows]
        return people_usernames
