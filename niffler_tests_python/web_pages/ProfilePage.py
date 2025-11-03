from urllib.parse import urljoin

from playwright.sync_api import Page, expect

from niffler_tests_python.settings.server_config import ServerConfig
from niffler_tests_python.web_pages.BasePage import BasePage
from niffler_tests_python.web_pages.components.NotificationComponent import NotificationComponent
from niffler_tests_python.web_pages.locators.ProfilePageLocators import ProfilePageLocators


class ProfilePage(BasePage):

    __url: str

    def __init__(self, page: Page, server_cfg: ServerConfig):
        super().__init__(page, server_cfg)
        self.locators = ProfilePageLocators
        self.notification = NotificationComponent(page, server_cfg)
        self.__url = urljoin(str(server_cfg.frontend_url), '/profile')

    def navigate(self):
        self._page.goto(self.__url)

    def expected_url(self):
        expect(self._page).to_have_url(self.__url)

    def reload(self):
        self._page.reload()

    def enter_add_category(self, category_name: str) -> None:
        category_input = self.locators.add_category_input(self._page)
        category_input.type(category_name)
        category_input.press('Enter')

    def click_add_category(self) -> None:
        self.locators.add_category_input(self._page).click()

    def submit_add_category(self) -> None:
        self.locators.add_category_input(self._page).press('Enter')

    def expected_add_input_empty(self) -> None:
        expect(self.locators.add_category_input(self._page)).to_have_value('')

    def expected_active_category_chip(self, category_name: str) -> None:
        expect(self.locators.active_category_chip(self._page, category_name)).to_be_visible()

    def expected_archive_category_chip(self, category_name: str) -> None:
        expect(self.locators.archive_category_chip(self._page, category_name)).to_be_visible()

    def click_edit_category_icon(self, category_name: str) -> None:
        self.locators.edit_icon_by_category(self._page, category_name).click()

    def click_archive_category_icon(self, category_name: str) -> None:
        self.locators.archive_icon_by_category(self._page, category_name).click()

    def click_unarchive_category_icon(self, category_name: str) -> None:
        self.locators.unarchive_icon_by_category(self._page, category_name).click()

    def expected_text_edit_category_input(self, category_name: str) -> None:
        expect(self.locators.edit_category_input(self._page)).to_have_value(category_name)

    def clear_edit_category_input(self) -> None:
        self.locators.edit_category_input(self._page).clear()

    def enter_edit_category(self, category_name: str) -> None:
        category_input = self.locators.edit_category_input(self._page)
        category_input.type(category_name)
        category_input.press('Enter')

    def click_category_chip(self, category_name: str) -> None:
        self.locators.category_chip(self._page, category_name).click()

    def click_close_edit_category_button(self) -> None:
        self.locators.close_edit_category_button(self._page).click()

    def clear_fullname_input(self) -> None:
        self.locators.fullname_input(self._page).clear()

    def enter_fullname(self, fullname: str) -> None:
        self.locators.fullname_input(self._page).type(fullname)

    def click_save_changes(self) -> None:
        self.locators.save_changes_button(self._page).click()

    def expect_archive_popup(self, category_name: str) -> None:
        expect(self.locators.popup_title(self._page)).to_have_text("Archive category")
        expect(self.locators.popup_description(self._page)).to_contain_text(
            f"Do you really want to archive {category_name}? After this change it won't be available while creating spends"
        )

    def expect_unarchive_popup(self, category_name: str) -> None:
        expect(self.locators.popup_title(self._page)).to_have_text("Unarchive category")
        expect(self.locators.popup_description(self._page)).to_contain_text(
            f"Do you really want to unarchive category {category_name}?"
        )

    def click_archive_category_button(self) -> None:
        self.locators.archive_category_button(self._page).click()

    def click_unarchive_category_button(self) -> None:
        self.locators.unarchive_category_button(self._page).click()

    def click_show_archived(self) -> None:
        self.locators.show_archived_button(self._page).click()

    def is_helper_text_add_category(self) -> None:
        expect(self.locators.helper_text_add_category(self._page)).to_be_visible()
