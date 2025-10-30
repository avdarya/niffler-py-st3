import pytest
from typing import Any
from collections.abc import Generator

from playwright.sync_api import Page, Browser, sync_playwright
from pytest import FixtureDef

from niffler_tests_python.settings.server_config import ServerConfig
from niffler_tests_python.web_pages.LoginPage import LoginPage


@pytest.fixture(scope='session')
def browser(server_cfg: ServerConfig) -> Generator[Browser, Any, Any]:
    with sync_playwright() as p:
        browser = getattr(p, server_cfg.browser_name).launch(
            headless=not server_cfg.headed
        )
        yield browser
        browser.close()

@pytest.fixture
def page_not_authed(browser: Browser) -> Generator[Page, Any, Any]:
    context = browser.new_context(locale='ru-RU')
    page = context.new_page()
    yield page
    context.close()

@pytest.fixture
def page_authed(browser: Browser, user: tuple[str, str], server_cfg: ServerConfig) -> Generator[Page, Any, Any]:
    context = browser.new_context(locale='ru-RU')
    page = context.new_page()
    username, password = user
    login_page = LoginPage(page, server_cfg)
    login_page.navigate()
    login_page.fill_username(username)
    login_page.fill_password(password)
    login_page.submit()
    yield page
    context.close()
