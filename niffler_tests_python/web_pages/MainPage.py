import json
from time import sleep

import allure
from allure_commons.types import AttachmentType
from playwright.sync_api import Page, expect, Locator
from selenium.common import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
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

    @allure.step('[UI /main] Get spend row: spend_id={spend_id}')
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

    @allure.step('[UI /main] Click edit icon')
    def click_edit_spend(self, spend_row: Locator) -> None:
        self.locators.edit_icon(spend_row).click()

    @allure.step('[UI /main] Click checkbox')
    def click_checkbox(self, spend_row: Locator) -> None:
        self.locators.checkbox(spend_row).click()

    @allure.step('[UI /main] Get checkbox state')
    def checkbox_should_checked(self, spend_row: Locator):
        expect(self.locators.checkbox(spend_row)).to_be_checked()

    @allure.step('[UI /main] Get checkbox state')
    def checkbox_should_unchecked(self, spend_row: Locator):
        expect(self.locators.checkbox(spend_row)).not_to_be_checked()

    @allure.step('[UI /main] Click delete button')
    def click_delete_button(self) -> None:
        self.locators.delete_button(self._page).click()

    @allure.step('[UI /main] Click submit delete button')
    def click_popup_delete_button(self) -> None:
        self.locators.popup_delete_button(self._page).click()

    @allure.step('[UI /main] Click select all rows')
    def select_all_rows(self) -> None:
        self.locators.checkbox_select_all(self._page).click()

    @allure.step('[UI /main] Get spend ids from selected rows')
    def get_selected_spend_ids(self) -> list[str]:
        spend_ids = []
        selected_rows = self.locators.selected_rows(self._page)
        for row in selected_rows:
            category_cell = self.locators.category_cell(row)
            spend_id = category_cell.get_attribute("id").replace("enhanced-table-checkbox-", "")
            spend_ids.append(spend_id)
        allure.attach(json.dumps(spend_ids, indent=2), name='Selected spend ids', attachment_type=AttachmentType.JSON)
        return spend_ids

    @allure.step('[UI /main] Get spend ids from rows')
    def get_spend_ids(self) -> list[str]:
        spend_ids = []
        expect(self.locators.row(self._page)).to_be_visible(timeout=5000)
        spend_rows = self.locators.rows(self._page)
        for row in spend_rows:
            category_cell = self.locators.category_cell(row)
            spend_id = category_cell.get_attribute("id").replace("enhanced-table-checkbox-", "")
            spend_ids.append(spend_id)
        allure.attach(json.dumps(spend_ids, indent=2), name='Spend ids', attachment_type=AttachmentType.JSON)
        return spend_ids

    @allure.step('[UI /main] Click cancel delete button')
    def click_popup_cancel_button(self) -> None:
        self.locators.popup_cancel_button(self._page).click()

    @allure.step('[UI /main] Click next page button')
    def click_next_button(self) -> None:
        self.locators.next_button(self._page).click()

    @allure.step('[UI /main] Click previous page button')
    def click_previous_button(self) -> None:
        first_row = self._page.locator('tbody tr').first
        first_text = first_row.text_content() if first_row.is_visible() else None

        self.locators.previous_button(self._page).click()

        if first_text:
            expect(first_row).not_to_have_text(first_text, timeout=5000)

    @allure.step('[UI /main] Enter search input: query={query}')
    def enter_search_query(self, query: str) -> None:
        search_input = self.locators.search_input(self._page)
        search_input.type(query)
        search_input.press('Enter')

    @allure.step('[UI /main] Get search input text')
    def get_search_query_input(self) -> str:
        return self.locators.search_input(self._page).input_value()

    @allure.step('[UI /main Click period field')
    def click_period_field(self) -> None:
        self.locators.period_field(self._page).click()

    @allure.step('[UI /main] Click period value: period={period}')
    def select_period_value(self, period: str) -> None:
        self.locators.period_option(self._page, period).click()

    @allure.step('[UI /main] Get period input text')
    def get_period_input(self) -> str:
        return self.locators.period_input(self._page).input_value()

    @allure.step('[UI /main] Click currency field')
    def click_currency_field(self) -> None:
        self.locators.currency_field(self._page).click()

    @allure.step('[UI /main] Click currency value: currency={currency}')
    def select_currency_value(self, currency: str) -> None:
        self.locators.currency_option(self._page, currency).click()

    @allure.step('[UI /main] Get currency input text')
    def get_currency_input(self) -> str:
        return self.locators.currency_input(self._page).input_value()

    # @allure.step('[UI /main] Open /main')
    # def open(self) -> None:
    #     self._driver.get(self.__url)
    #     self._driver.refresh()
    #     self.wait_for(self.locator.NIFFLER_IMG)
    #
    #
    # @allure.step('[UI /main] Get checkbox state')
    # def get_checkbox_state(self, spend_row: WebElement) -> bool:
    #     checked = spend_row.get_attribute('aria-checked')
    #     result = checked == "true"
    #     allure.attach(str(result), name='Checkbox State', attachment_type=AttachmentType.TEXT)
    #     return result
    #
    # @allure.step('[UI /main] Click checkbox')
    # def click_checkbox(self, spend_row: WebElement) -> None:
    #     spend_row.find_element(*self.locator.CHECKBOX).click()
    #
    # @allure.step('[UI /main] Click select all rows')
    # def click_select_all_rows(self) -> None:
    #     self._driver.find_element(*self.locator.MULTI_SELECT_CHECKBOX).click()
    #
    # @allure.step('[UI /main] Click edit icon')
    # def click_edit_spend(self, spend_row: WebElement) -> None:
    #     spend_row.find_element(*self.locator.EDIT_ICON).click()
    #     self.wait_for(self.locator.AMOUNT_INPUT)
    #
    # @allure.step('[UI /main] Click delete button')
    # def click_delete_spend(self) -> None:
    #     self._driver.find_element(*self.locator.DELETE_BUTTON).click()
    #
    # @allure.step('[UI /main] Click submit delete button')
    # def click_submit_delete_spend(self) -> None:
    #     submit_popup = self.wait_for(self.locator.SUBMIT_POPUP, EC.visibility_of_element_located)
    #     submit_popup.find_element(*self.locator.SUBMIT_DELETE_BUTTON).click()
    #
    # @allure.step('[UI /main] Click cancel delete button')
    # def click_cancel_delete_spend(self) -> None:
    #     submit_popup = self.wait_for(self.locator.SUBMIT_POPUP, EC.visibility_of_element_located)
    #     submit_popup.find_element(*self.locator.CANCEL_DELETE_BUTTON).click()
    #
    # @allure.step('[UI /main] Click next page button')
    # def click_next_page(self) -> None:
    #     self._driver.find_element(*self.locator.NEXT_PAGE_BUTTON).click()
    #
    # @allure.step('[UI /main] Click previous page button')
    # def click_previous_page(self) -> None:
    #     try:
    #         first_row = self._driver.find_element(*self.locator.CATEGORY_CELL)
    #         prev_button = self.wait_for(self.locator.PREVIOUS_PAGE_BUTTON, EC.element_to_be_clickable)
    #         prev_button.click()
    #         self.wait_for_staleness(first_row)
    #     except (StaleElementReferenceException, NoSuchElementException):
    #         pass
    #     self.wait_for(self.locator.CATEGORY_CELL, EC.presence_of_all_elements_located)
    #
    # @allure.step('[UI /main] Get alert text')
    # def alert_on_action(self) -> str:
    #     alert = self.wait_for(self.locator.ALERT_DIALOG, EC.visibility_of_element_located)
    #     allure.attach(alert.text, name='Alert text', attachment_type=AttachmentType.TEXT)
    #     return alert.text
    #
    # @allure.step('[UI /main Click period field')
    # def click_period_field(self) -> None:
    #     self._driver.find_element(*self.locator.PERIOD_FIELD).click()
    #
    # @allure.step('[UI /main] Click period value: period={period}')
    # def click_period_value(self, period: str) -> None:
    #     self._driver.find_element(self.locator.PERIOD_VALUE[0],  self.locator.PERIOD_VALUE[1].format(period)).click()
    #
    # @allure.step('[UI /main] Click currency field')
    # def click_currency_field(self) -> None:
    #     self._driver.find_element(*self.locator.CURRENCY_FIELD).click()
    #
    # @allure.step('[UI /main] Click currency value: currency={currency}')
    # def click_currency_value(self, currency: str) -> None:
    #     self._driver.find_element(self.locator.CURRENCY_VALUE[0], self.locator.CURRENCY_VALUE[1].format(currency),).click()
    #
    # @allure.step('[UI /main] Enter search input: query={query}')
    # def enter_search_query(self, query: str) -> None:
    #     query_input = self._driver.find_element(*self.locator.SEARCH_INPUT)
    #     query_input.send_keys(query)
    #     query_input.send_keys(Keys.ENTER)
    #
    # @allure.step('[UI /main] Get search input text')
    # def get_search_query_input(self) -> str:
    #     query_input = self._driver.find_element(*self.locator.SEARCH_INPUT)
    #     input_value = query_input.get_attribute('value')
    #     allure.attach(input_value, name='Search input text', attachment_type=AttachmentType.TEXT)
    #     return input_value
    #
    # @allure.step('[UI /main] Get period input text')
    # def get_period_input(self) -> str:
    #     period_input = self._driver.find_element(*self.locator.PERIOD_INPUT)
    #     input_value = period_input.get_attribute('value')
    #     allure.attach(input_value, name='Search input text', attachment_type=AttachmentType.TEXT)
    #     return input_value
    #
    # @allure.step('[UI /main] Get currency input text')
    # def get_currency_input(self) -> str:
    #     currency_input = self._driver.find_element(*self.locator.CURRENCY_INPUT)
    #     input_value = currency_input.get_attribute('value')
    #     allure.attach(input_value, name='Search input text', attachment_type=AttachmentType.TEXT)
    #     return input_value
    #
    # @allure.step('[UI /main] Get spend ids from rows')
    # def get_spend_ids_row(self) -> list[str]:
    #     spend_ids = []
    #     elements = self.wait_for(self.locator.CATEGORY_CELL, EC.visibility_of_any_elements_located)
    #     for e in elements:
    #         spend_id = e.get_attribute("id").replace("enhanced-table-checkbox-", "")
    #         spend_ids.append(spend_id)
    #     allure.attach(json.dumps(spend_ids, indent=2), name='Spend ids', attachment_type=AttachmentType.JSON)
    #     return spend_ids
    #
    # @allure.step('[UI /main] Get spend ids from selected rows')
    # def get_selected_spend_ids_row(self) -> list[str]:
    #     spend_ids = []
    #     selected_rows = self._driver.find_elements(*self.locator.SELECTED_SPEND_ROW)
    #
    #     for spend in selected_rows:
    #         spend_checkbox = spend.find_element(*self.locator.CATEGORY_CELL)
    #         spend_id = spend_checkbox.get_attribute("id").replace("enhanced-table-checkbox-", "")
    #         spend_ids.append(spend_id)
    #     allure.attach(json.dumps(spend_ids, indent=2), name='Selected spend ids', attachment_type=AttachmentType.JSON)
    #     return spend_ids
    #
    # @allure.step('[UI /main] Get spend row: spend_id={spend_id}')
    # def get_spend_row(self, spend_id: str) -> WebElement | None:
    #     try:
    #         img_lonely_niffler = self._driver.find_element(*self.locator.LONELY_NIFFLER_IMG)
    #         if img_lonely_niffler.is_displayed():
    #             return None
    #     except NoSuchElementException:
    #         pass
    #     while True:
    #         spend_rows = self._driver.find_elements(*self.locator.SPEND_ROW)
    #         first_row_category_id = (spend_rows[0]
    #             .find_element(*self.locator.CATEGORY_CELL_FROM_CATEGORY)
    #             .get_attribute('id')
    #         )
    #         first_row_category = self._driver.find_element(By.ID, first_row_category_id)
    #         try:
    #             td = self._driver.find_element(
    #                 self.locator.CATEGORY_CELL_BY_ID[0],
    #                 self.locator.CATEGORY_CELL_BY_ID[1].format(spend_id),
    #             )
    #             row = td.find_element(*self.locator.SPEND_ROW_FROM_CATEGORY)
    #             return row
    #         except NoSuchElementException:
    #             pass
    #
    #         try:
    #             next_page_button = self._driver.find_element(*self.locator.NEXT_PAGE_BUTTON)
    #             if (
    #                     next_page_button.get_attribute("disabled") is not None or
    #                     "disabled" in next_page_button.get_attribute("class")
    #             ):
    #                 break
    #             next_page_button.click()
    #             WebDriverWait(self._driver, self._timeout).until(
    #                 EC.staleness_of(first_row_category)
    #             )
    #         except Exception:
    #             break
    #
    #     return None

    @allure.step('[UI /main] Open /main')
    def navigate(self) -> None:
        self._page.goto(self.__url)
        # self._driver.refresh()
        # self.wait_for(self.locator.NIFFLER_IMG)

    def is_correct_url(self):
        expect(self._page).to_have_url(self.__url)

