from dataclasses import dataclass

from playwright.sync_api import Page, Locator
from selenium.webdriver.common.by import By


@dataclass(frozen=True)
class ProfilePageLocators:
    # FULLNAME_INTPUT = (By.ID, 'name')
    # ADD_CATEGORY_INPUT = (By.CSS_SELECTOR, 'input[placeholder="Add new category"]')
    # EDIT_CATEGORY_INPUT = (By.CSS_SELECTOR, 'input[placeholder="Edit category"]')
    # CATEGORY_CHIP_BY_NAME = (By.XPATH, '//div[contains(@class, "MuiChip-clickable") and .//span[text()="{}"]]')
    # CATEGORY_CHIP = (By.CSS_SELECTOR, 'div.MuiChip-root[role="button"]')
    # CATEGORY_BOX = (By.XPATH, '//span[text()="{}"]/ancestor::div[contains(@class, "MuiBox-root")]')
    # EDIT_ICON = (By.CSS_SELECTOR, 'button[aria-label="Edit category"]')
    # CLOSE_ICON = (By.CSS_SELECTOR, 'button[aria-label="close"]')
    # ARCHIVE_ICON = (By.CSS_SELECTOR, 'button[aria-label="Archive category"]')
    # UNARCHIVE_ICON = (By.CSS_SELECTOR, 'button[aria-label="Unarchive category"]')
    # SUBMIT_ARCHIVE_BUTTON = (By.XPATH, '//button[normalize-space()="Archive"]')
    # SUBMIT_UNARCHIVE_BUTTON = (By.XPATH, '//button[normalize-space()="Unarchive"]')
    # SAVE_CHANGES_BUTTON = (By.CSS_SELECTOR, 'button[type="submit"]')
    # SHOW_ARCHIVED_BUTTON = (By.CSS_SELECTOR, 'input[type="checkbox"]')
    # SUBMIT_POPUP = (By.CSS_SELECTOR, 'div[aria-describedby="alert-dialog-slide-description"]')
    # POPUP_DESCRIPTION = (By.CSS_SELECTOR, 'p[id="alert-dialog-slide-description"]')
    # POPUP_TITLE = (By.CSS_SELECTOR, 'h2')
    # ALERT_DIALOG = (By.CSS_SELECTOR, 'div[role="alert"]')
    # ADD_CATEGORY_HELPER_TEXT = (By.CSS_SELECTOR, 'input[placeholder="Add new category"] + span.input__helper-text')

    @staticmethod
    def add_category_input(page: Page) -> Locator:
        return page.get_by_placeholder('Add new category')

    @staticmethod
    def edit_category_input(page: Page) -> Locator:
        return page.get_by_placeholder('Edit category')

    @staticmethod
    def active_category_chip(page: Page, category_name: str) -> Locator:
        return page.locator(
            f'//div[contains(@class,"MuiChip-root") and contains(@class,"MuiChip-colorPrimary")]'
            f'//span[text()="{category_name}"]'
        )

    @staticmethod
    def archive_category_chip(page: Page, category_name: str) -> Locator:
        return page.locator(
            f'//div[contains(@class,"MuiChip-root") and contains(@class,"MuiChip-colorDefault")]'
            f'//span[text()="{category_name}"]'
        )

    @staticmethod
    def category_chip(page: Page, category_name: str) -> Locator:
        return page.locator(f'//div[contains(@class,"MuiChip-root") and .//span[text()="{category_name}"]]')

    @staticmethod
    def edit_icon_by_category(page: Page, category_name: str) -> Locator:
        return page.locator(
            f'//div[contains(@class,"MuiChip-root") and .//span[text()="{category_name}"]]'
            '/following-sibling::div//button[@aria-label="Edit category"]'
        )

    @staticmethod
    def archive_icon_by_category(page: Page, category_name: str) -> Locator:
        return page.locator(
            f'//div[contains(@class,"MuiChip-root") and .//span[text()="{category_name}"]]'
            '/following-sibling::div//button[@aria-label="Archive category"]'
        )

    @staticmethod
    def unarchive_icon_by_category(page: Page, category_name: str) -> Locator:
        return page.locator(
            f'//div[contains(@class,"MuiChip-root") and .//span[text()="{category_name}"]]'
            '/following-sibling::span/button[@aria-label="Unarchive category"]'
        )

    @staticmethod
    def close_edit_category_button(page: Page) -> Locator:
        return page.locator('button[aria-label="close"]')

    @staticmethod
    def popup_title(page: Page) -> Locator:
        return page.locator('div[role="dialog"] h2')

    @staticmethod
    def popup_description(page: Page) -> Locator:
        return page.locator('#alert-dialog-slide-description')

    @staticmethod
    def archive_category_button(page: Page) -> Locator:
        return page.locator('//button[normalize-space()="Archive"]')

    @staticmethod
    def unarchive_category_button(page: Page) -> Locator:
        return page.locator('//button[normalize-space()="Unarchive"]')

    @staticmethod
    def show_archived_button(page: Page) -> Locator:
        return page.get_by_label("Show archived")

    @staticmethod
    def helper_text_add_category(page: Page) -> Locator:
        return page.get_by_text('Allowed category length is from 2 to 50 symbols')