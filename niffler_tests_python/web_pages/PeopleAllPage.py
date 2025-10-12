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
        while True:
            row = self.locators.people_row(self._page, name)
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
