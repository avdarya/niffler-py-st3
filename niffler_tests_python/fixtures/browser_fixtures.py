import datetime
import uuid
import allure
import pytest
from typing import Callable, Any, Generator
from collections.abc import Generator

from allure_commons.reporter import AllureReporter
from allure_pytest.listener import AllureListener
from faker import Faker
from playwright.sync_api import Page, Browser, sync_playwright
from pydantic import SecretStr
from pytest import Item, FixtureDef, FixtureRequest
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from niffler_tests_python.clients.kafka_client import KafkaClient
from niffler_tests_python.clients.oauth_client import OAuthClient
from niffler_tests_python.databases.auth_db import AuthDB
from niffler_tests_python.databases.user_db import UserDB
from niffler_tests_python.settings.client_config import ClientConfig
from niffler_tests_python.settings.server_config import ServerConfig
from niffler_tests_python.web_pages.LoginPage import LoginPage
from niffler_tests_python.web_pages.RegisterPage import RegisterPage


@pytest.fixture(scope='session')
def browser(server_cfg: ServerConfig) -> Generator[Browser, Any, Any]:
    with sync_playwright() as p:
        browser = getattr(p, server_cfg.browser_name).launch(
            headless=not server_cfg.headed
        )
        yield browser
        browser.close()

# @pytest.fixture(scope='session')
# def storage_state_path(
#         tmp_path_factory,
#         browser: Browser,
#         auth_token_factory,
#         server_cfg: ServerConfig,
#         user: tuple[str, str]
# ) -> str:
#     state_file = tmp_path_factory.mktemp("state") / "auth_state.json"
#     context = browser.new_context()
#     username, password = user
#     token = auth_token_factory( username, password)
#
#     context.add_init_script(f"""
#         window.localStorage.setItem("id_token", "{token}");
#     """)
#
#     page = context.new_page()
#     page.goto(str(server_cfg.frontend_url))
#     page.wait_for_load_state("networkidle")
#
#     context.storage_state(path=state_file)
#     context.close()
#     return str(state_file)

@pytest.fixture
def page_not_authed(browser: Browser) -> Generator[Page, Any, Any]:
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()
#
# @pytest.fixture(scope='session')
# def page_authed(browser: Browser, storage_state_path: str) -> Generator[Page, Any, Any]:
#     context = browser.new_context(storage_state=storage_state_path)
#     page = context.new_page()
#     yield page
#     context.close()


@pytest.fixture(scope='session')
def page_authed(browser: Browser, user: tuple[str, str], server_cfg: ServerConfig) -> Generator[Page, Any, Any]:
    context = browser.new_context()
    page = context.new_page()
    username, password = user
    login_page = LoginPage(page, server_cfg)
    login_page.navigate()
    login_page.fill_username(username)
    login_page.fill_password(password)
    login_page.submit()
    yield page
    context.close()