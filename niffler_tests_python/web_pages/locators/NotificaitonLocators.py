from dataclasses import dataclass

from playwright.sync_api import Locator, Page


@dataclass(frozen=True)
class NotificationLocators:

    @staticmethod
    def message(page: Page) -> Locator:
        return page.locator('div[role="alert"] .MuiAlert-message')

    @staticmethod
    def success(page: Page) -> Locator:
        return page.locator('div.MuiAlert-standardSuccess[role="alert"]')

    @staticmethod
    def error(page: Page) -> Locator:
        return page.locator('div.MuiAlert-standardError[role="alert"]')

    @staticmethod
    def info(page: Page) -> Locator:
        return page.locator('div.MuiAlert-standardInfo[role="alert"]')
