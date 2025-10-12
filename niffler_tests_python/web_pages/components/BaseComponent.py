from playwright.sync_api import Page

from niffler_tests_python.settings.server_config import ServerConfig


class BaseComponent:

    _page: Page
    _timeout: float
    _poll: float

    def __init__(self, page: Page,  server_cfg: ServerConfig):
        self._page = page
        self._timeout = server_cfg.timeout
        self._poll = server_cfg.poll
