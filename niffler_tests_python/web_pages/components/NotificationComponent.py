from playwright.sync_api import Page, expect

from niffler_tests_python.settings.server_config import ServerConfig
from niffler_tests_python.web_pages.components.BaseComponent import BaseComponent
from niffler_tests_python.web_pages.locators.NotificaitonLocators import NotificationLocators


class NotificationComponent(BaseComponent):

    def __init__(self, page: Page, server_cfg: ServerConfig):
        super().__init__(page, server_cfg)
        self.locators = NotificationLocators

    def get_notification_text(self) -> str:
        return self.locators.message(self._page).inner_text()

    def is_success_notification(self) -> None:
        expect(self.locators.success(self._page)).to_be_visible()

    def is_error_notification(self) -> None:
        expect(self.locators.error(self._page)).to_be_visible()

    def is_info_notification(self) -> None:
        expect(self.locators.info(self._page)).to_be_visible()