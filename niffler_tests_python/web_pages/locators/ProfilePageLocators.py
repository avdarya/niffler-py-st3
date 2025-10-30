from dataclasses import dataclass

from playwright.sync_api import Page, Locator
from selenium.webdriver.common.by import By


@dataclass(frozen=True)
class ProfilePageLocators:

    @staticmethod
    def add_category_input(page: Page) -> Locator:
        return page.get_by_placeholder('Add new category')

    @staticmethod
    def fullname_input(page: Page) -> Locator:
        return page.locator('#name')

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

    @staticmethod
    def save_changes_button(page: Page) -> Locator:
        return page.get_by_role('button', name='Save changes')