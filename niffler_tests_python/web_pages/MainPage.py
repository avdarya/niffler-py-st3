import json

from allure_commons.types import AttachmentType
from playwright.sync_api import Page, expect, Locator
from selenium.common import NoSuchElementException
from urllib.parse import urljoin

from niffler_tests_python.settings.server_config import ServerConfig
from niffler_tests_python.web_pages.BasePage import BasePage
from niffler_tests_python.web_pages.components.NotificationComponent import NotificationComponent
from niffler_tests_python.web_pages.locators.MainPageLocators import MainPageLocators


class MainPage(BasePage):

    __url: str

    def __init__(self, page: Page, server_cfg: ServerConfig) -> None:
        super().__init__(page, server_cfg)
        self.locators = MainPageLocators
        self.notification = NotificationComponent(page, server_cfg)
        self.__url = urljoin(str(server_cfg.frontend_url),'/main')

    def navigate(self):
        self._page.goto(self.__url)

    def expected_url(self):
        expect(self._page).to_have_url(self.__url)

    def reload(self):
        self._page.reload()

    def get_spend_row_by_id(self, spend_id: str) -> Locator | None:
        try:
            img_lonely_niffler = self.locators.img_lonely_niffler(self._page)
            if img_lonely_niffler.is_visible():
                return None
        except NoSuchElementException:
            pass
        while True:
            row = self.locators.spend_row_by_id(self._page, spend_id)
            row.wait_for(state="visible", timeout=5000)
            if row.is_visible():
                return row
            if self.locators.next_button(self._page).get_attribute('disabled') is not None:
                return None
            first_row = self._page.locator('tbody tr').first
            first_text = first_row.text_content()
            self.click_next_button()
            first_row.wait_for(state="visible")
            expect(first_row).not_to_have_text(first_text, timeout=5000)

    def click_edit_spend(self, spend_row: Locator) -> None:
        self.locators.edit_icon(spend_row).click()

    def click_checkbox(self, spend_row: Locator) -> None:
        self.locators.checkbox(spend_row).click()

    def checkbox_should_checked(self, spend_row: Locator):
        expect(self.locators.checkbox(spend_row)).to_be_checked()

    def checkbox_should_unchecked(self, spend_row: Locator):
        expect(self.locators.checkbox(spend_row)).not_to_be_checked()

    def click_delete_button(self) -> None:
        self.locators.delete_button(self._page).click()

    def click_popup_delete_button(self) -> None:
        self.locators.popup_delete_button(self._page).click()

    def select_all_rows(self) -> None:
        self.locators.checkbox_select_all(self._page).click()

    def get_selected_spend_ids(self) -> list[str]:
        spend_ids = []
        selected_rows = self.locators.selected_rows(self._page)
        for row in selected_rows:
            category_cell = self.locators.category_cell(row)
            spend_id = category_cell.get_attribute("id").replace("enhanced-table-checkbox-", "")
            spend_ids.append(spend_id)
        # allure.attach(json.dumps(spend_ids, indent=2), name='Selected spend ids', attachment_type=AttachmentType.JSON)
        return spend_ids

    def get_spend_ids(self) -> list[str]:
        spend_ids = []
        self._page.wait_for_selector(self.locators.first_category_cell(), timeout=10000)
        spend_rows = self.locators.rows(self._page)
        for row in spend_rows:
            category_cell = self.locators.category_cell(row)
            spend_id = category_cell.get_attribute("id").replace("enhanced-table-checkbox-", "")
            spend_ids.append(spend_id)
        # allure.attach(json.dumps(spend_ids, indent=2), name='Spend ids', attachment_type=AttachmentType.JSON)
        return spend_ids

    def click_popup_cancel_button(self) -> None:
        self.locators.popup_cancel_button(self._page).click()

    def click_next_button(self) -> None:
        self.locators.next_button(self._page).click()
        self._wait_table_updated()

    def click_previous_button(self) -> None:
        first_row = self._page.locator('tbody tr').first
        first_text = first_row.text_content() if first_row.is_visible() else None

        self.locators.previous_button(self._page).click()

        if first_text:
            expect(first_row).not_to_have_text(first_text, timeout=5000)
        self._wait_table_updated()

    def enter_search_query(self, query: str) -> None:
        search_input = self.locators.search_input(self._page)
        search_input.type(query)
        search_input.press('Enter')
        self._wait_table_updated()

    def get_search_query_input(self) -> str:
        return self.locators.search_input(self._page).input_value()

    def click_period_field(self) -> None:
        self.locators.period_field(self._page).click()

    def select_period_value(self, period: str) -> None:
        self.locators.period_option(self._page, period).click()
        self._wait_table_updated()

    def get_period_input(self) -> str:
        return self.locators.period_input(self._page).input_value()

    def click_currency_field(self) -> None:
        self.locators.currency_field(self._page).click()

    def select_currency_value(self, currency: str) -> None:
        self.locators.currency_option(self._page, currency).click()
        self._wait_table_updated()

    def get_currency_input(self) -> str:
        return self.locators.currency_input(self._page).input_value()

    def is_correct_url(self):
        expect(self._page).to_have_url(self.__url)

    def _wait_table_updated(self, timeout: int = 5000):
        first_row = self.locators.row(self._page)
        if not first_row.is_visible():
            self.locators.row(self._page).wait_for(timeout=timeout)
            return
        old_text = first_row.text_content()
        try:
            expect(first_row).not_to_have_text(old_text, timeout=timeout)
        except AssertionError:
            self._page.wait_for_load_state("networkidle", timeout=timeout)
