from playwright.sync_api import Page, expect
from niffler_tests_python.settings.server_config import ServerConfig
from niffler_tests_python.web_pages.components.BaseComponent import BaseComponent
from niffler_tests_python.web_pages.locators.HeaderLocators import HeaderLocators


class HeaderComponent(BaseComponent):

    def __init__(self, page: Page,  server_cfg: ServerConfig):
        super().__init__(page, server_cfg)
        self.locators = HeaderLocators

    def click_new_spending(self) -> None:
        self.locators.spending_button(self._page).click()

    def is_visible_person_icon(self):
        expect(self.locators.person_icon(self._page)).to_be_visible()

    def click_person_icon(self) -> None:
        self.locators.person_icon(self._page).click()

    def click_profile_button(self) -> None:
        self.locators.profile_button(self._page).click()

    def click_friends_button(self) -> None:
        self.locators.friends_button(self._page).click()

    def click_all_people(self) -> None:
        self.locators.all_people_button(self._page).click()
