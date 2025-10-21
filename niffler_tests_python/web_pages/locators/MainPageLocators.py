from dataclasses import dataclass

from playwright.sync_api import Page, Locator


@dataclass(frozen=True)
class MainPageLocators:
    # NIFFLER_IMG = (By.CSS_SELECTOR, 'img[alt="Niffler logo"]')
    # LONELY_NIFFLER_IMG = (By.CSS_SELECTOR, 'img[alt="Lonely niffler"')
    # CHECKBOX = (By.CSS_SELECTOR, 'input[type="checkbox"]')
    # MULTI_SELECT_CHECKBOX = (By.CSS_SELECTOR, 'input[aria-label="select all rows"]')
    # EDIT_ICON = (By.CSS_SELECTOR,'button[aria-label="Edit spending"]')
    # AMOUNT_INPUT = ( By.ID, 'amount')
    # DELETE_BUTTON = (By.ID, 'delete')
    # SUBMIT_POPUP = (By.CSS_SELECTOR, 'div[aria-describedby="alert-dialog-slide-description"]')
    # SUBMIT_DELETE_BUTTON = (By.XPATH, './/button[normalize-space(text())="Delete"]')
    # CANCEL_DELETE_BUTTON = (By.XPATH, './/button[normalize-space(text())="Cancel"]')
    # NEXT_PAGE_BUTTON = (By.ID, 'page-next')
    # PREVIOUS_PAGE_BUTTON = (By.ID, 'page-prev')
    # ALERT_DIALOG = (By.CSS_SELECTOR, 'div[role="alert"]')
    # PERIOD_FIELD = (By.ID, 'period')
    # PERIOD_VALUE = (By.CSS_SELECTOR, 'li[data-value="{}"]')
    # PERIOD_INPUT = (By.CSS_SELECTOR, 'input[name="period"]')
    # CURRENCY_FIELD = (By.ID, 'currency')
    # CURRENCY_VALUE = (By.CSS_SELECTOR, 'li[data-value="{}"]')
    # CURRENCY_INPUT = (By.CSS_SELECTOR, 'input[name="currency"]')
    # SEARCH_INPUT = (By.CSS_SELECTOR, 'input[aria-label="search"]')
    # CATEGORY_CELL = (By.CSS_SELECTOR, 'td[id^="enhanced-table-checkbox-"]')
    # CATEGORY_CELL_FROM_CATEGORY = (By.XPATH, '//td[contains(@id, "enhanced-table-checkbox")]')
    # CATEGORY_CELL_BY_ID = (By.CSS_SELECTOR, 'td[id="enhanced-table-checkbox-{}"]')
    # SPEND_ROW = (By.CSS_SELECTOR, "tr.MuiTableRow-root")
    # SPEND_ROW_FROM_CATEGORY = (By.XPATH, './ancestor::tr')
    # SELECTED_SPEND_ROW = (By.CSS_SELECTOR, 'tr[aria-checked="true"]')

    @staticmethod
    def spend_row_by_id(page: Page, spend_id: str) -> Locator:
        return page.locator(f'td#enhanced-table-checkbox-{spend_id}').locator("..")

    @staticmethod
    def img_lonely_niffler(page: Page) -> Locator:
        return page.get_by_alt_text('Lonely niffler')

    @staticmethod
    def next_button(page: Page) -> Locator:
        return page.locator('#page-next')

    @staticmethod
    def previous_button(page: Page) -> Locator:
        return page.locator('#page-prev')

    @staticmethod
    def edit_icon(spend_row: Locator) -> Locator:
        return spend_row.get_by_role('button', name='Edit spending')

    @staticmethod
    def checkbox(spend_row: Locator) -> Locator:
        return spend_row.get_by_role('checkbox')

    @staticmethod
    def selected_rows(page: Page) -> list[Locator]:
        return page.locator('tr[aria-checked="true"]').all()

    @staticmethod
    def rows(page: Page) -> list[Locator]:
        return page.locator("tbody tr.MuiTableRow-root").all()

    @staticmethod
    def row(page: Page) -> Locator:
        return page.locator("tbody tr.MuiTableRow-root").first

    @staticmethod
    def delete_button(page: Page) -> Locator:
        return page.locator('#delete')

    @staticmethod
    def popup_delete_button(page: Page) -> Locator:
        return page.get_by_role("dialog").get_by_role("button", name="Delete")

    @staticmethod
    def popup_cancel_button(page: Page) -> Locator:
        return page.get_by_role("dialog").get_by_role("button", name="Cancel")

    @staticmethod
    def checkbox_select_all(page: Page) -> Locator:
        return page.get_by_role('checkbox', name='select all rows')

    @staticmethod
    def first_category_cell() -> str:
        return "tbody tr.MuiTableRow-root td[id^='enhanced-table-checkbox-']"

    @staticmethod
    def category_cell(row: Locator) -> Locator:
        return row.locator('td[id^="enhanced-table-checkbox-"]')

    @staticmethod
    def search_input(page: Page) -> Locator:
        return page.locator('input[aria-label="search"]')

    @staticmethod
    def period_field(page: Page) -> Locator:
        return page.locator('#period')

    @staticmethod
    def period_option(page: Page, period: str) -> Locator:
        return page.locator(f'li[data-value="{period}"]')

    @staticmethod
    def period_input(page: Page) -> Locator:
        return page.locator('input[name="period"]')

    @staticmethod
    def currency_field(page: Page) -> Locator:
        return page.locator('#currency')

    @staticmethod
    def currency_option(page: Page, currency: str) -> Locator:
        return page.locator(f'li[data-value="{currency}"]')

    @staticmethod
    def currency_input(page: Page) -> Locator:
        return page.locator('input[name="currency"]')

