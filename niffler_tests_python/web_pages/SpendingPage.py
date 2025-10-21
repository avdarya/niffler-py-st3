from urllib.parse import urljoin

from playwright.sync_api import Page, expect

from niffler_tests_python.settings.server_config import ServerConfig
from niffler_tests_python.web_pages.BasePage import BasePage
from niffler_tests_python.web_pages.locators.SpendingPageLocators import SpendingPageLocators


class SpendingPage(BasePage):

    __url: str

    def __init__(self, page: Page,  server_cfg: ServerConfig):
        super().__init__(page, server_cfg)
        self.locators = SpendingPageLocators
        self.__url = urljoin(str(server_cfg.frontend_url), '/spending')

    def navigate(self):
        self._page.goto(self.__url)

    def expected_url(self):
        expect(self._page).to_have_url(self.__url)

    def expected_spend_url(self, spend_id: str):
        expect(self._page).to_have_url(f'{self.__url}/{spend_id}')

    def fill_amount(self, amount: str) -> None:
        self.locators.amount_input(self._page).type(amount)

    def clear_amount(self) -> None:
        self.locators.amount_input(self._page).clear()

    def click_currency(self) -> None:
        self.locators.currency_field(self._page).click()

    def select_currency(self, currency: str) -> None:
        self.locators.currency_option(self._page, currency).click()

    def fill_category(self, category: str) -> None:
        self.locators.category_input(self._page).type(category)

    def fill_date(self, spend_date: str) -> None:
        self.locators.date_input(self._page).click()
        self.locators.date_input(self._page).type(spend_date)

    def fill_description(self, description: str) -> None:
        self.locators.description_input(self._page).type(description)

    def submit_form(self) -> None:
        self.locators.submit(self._page).click()

    def click_cancel(self) -> None:
        self.locators.cancel_button(self._page).click()

    def clear_category_input(self) -> None:
        self.locators.category_input(self._page).clear()

    def clear_description_input(self) -> None:
        self.locators.description_input(self._page).clear()

    def is_helper_text_amount_shown(self) -> None:
        expect(self.locators.helper_text_amount(self._page)).to_be_visible()

    def is_helper_text_category_shown(self) -> None:
        expect(self.locators.helper_text_category(self._page)).to_be_visible()

    def get_amount_input(self) -> str:
        return self.locators.amount_input(self._page).get_attribute('value')

    def get_selected_currency_input(self) -> str:
        return self.locators.currency_input(self._page).input_value()

    def get_category_input(self) -> str:
        return self.locators.category_input(self._page).input_value()

    def get_description_input(self) -> str:
        return self.locators.description_input(self._page).input_value()

    def get_date_input(self) -> str:
        return self.locators.date_input(self._page).input_value()
