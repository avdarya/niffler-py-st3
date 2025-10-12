from dataclasses import dataclass

from playwright.sync_api import Page, Locator


@dataclass(frozen=True)
class SpendingPageLocators:
    # AMOUNT_INPUT = (By.ID, 'amount')
    # AMOUNT_FIELD = (By.XPATH, './/input[@id="amount"]/parent::div')
    # AMOUNT_INPUT_HELPER_TEXT = (By.CSS_SELECTOR, '.input__helper-text')
    # DESCRIPTION_INPUT = (By.ID, 'description')
    # DATE_INPUT = (By.CSS_SELECTOR, 'input[name="date"]')
    # CURRENCY_FIELD = (By.CSS_SELECTOR, 'div[aria-labelledby="currency"]')
    # CURRENCY_INPUT = (By.ID, 'currency')
    # CURRENCY_DIALOG = (By.CSS_SELECTOR, 'ul[role="listbox"]')
    # CURRENCY_VALUE = (By.CSS_SELECTOR, 'li[data-value="{}"]')
    # CATEGORY_INPUT = (By.ID, 'category')
    # CATEGORY_FIELD = (By.XPATH, './/input[@id="category"]/parent::div')
    # CATEGORY_CHIP = (By.XPATH, '//span[contains(@class, "MuiChip-label") and text()="{}"]')
    # HELPER_TEXT = (By.CSS_SELECTOR, '.input__helper-text')
    # ADD_BUTTON = (By.CSS_SELECTOR, 'button[id="save"]')

    @staticmethod
    def amount_input(page: Page) -> Locator:
        return page.locator("#amount")

    @staticmethod
    def currency_field(page: Page) -> Locator:
        return page.locator("#currency")

    @staticmethod
    def currency_option(page: Page, value: str) -> Locator:
        return page.locator(f'li[role="option"][data-value="{value}"]')

    @staticmethod
    def currency_input(page: Page) -> Locator:
        return page.locator('input[name="currency"]')

    @staticmethod
    def category_input(page: Page) -> Locator:
        return page.locator('#category')

    @staticmethod
    def date_input(page: Page) -> Locator:
        return page.locator('input[name="date"]')

    @staticmethod
    def description_input(page: Page) -> Locator:
        return page.locator('#description')

    @staticmethod
    def submit(page: Page) -> Locator:
        return page.locator("#save")

    @staticmethod
    def helper_text_amount(page: Page) -> Locator:
        return page.get_by_text('Amount has to be not less then 0.01')

    @staticmethod
    def helper_text_category(page: Page) -> Locator:
        return page.get_by_text('Please choose category')

    @staticmethod
    def cancel_button(page: Page) -> Locator:
        return page.locator('#cancel')