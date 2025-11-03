from dataclasses import dataclass

from playwright.sync_api import Page, Locator


@dataclass(frozen=True)
class MainPageLocators:

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

