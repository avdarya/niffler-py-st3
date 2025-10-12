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
from niffler_tests_python.tests.conftest import server_cfg
from niffler_tests_python.web_pages.LoginPage import LoginPage
from niffler_tests_python.web_pages.RegisterPage import RegisterPage


@pytest.fixture
def generate_username(fake: Faker) -> Callable[[str], str]:
    return fake.user_name()

@pytest.fixture
def generate_password(fake: Faker) -> Callable[[str], str]:
    return fake.password()

@pytest.fixture
def username_with_teardown(
        auth_db: AuthDB,
        userdata_db: UserDB,
        request: FixtureRequest,
        fake: Faker
) -> str:
    username = fake.user_name()

    def fin():
        userdata_db.delete_user(username)
        auth_db.delete_by_username(username)

    request.addfinalizer(fin)
    return username

@pytest.fixture
def register_new_user(
        auth_client: OAuthClient,
        auth_db: AuthDB,
        user_db: UserDB,
        request: FixtureRequest,
        generate_username: str,
        generate_password: str
) -> tuple[str, str]:
    auth_client.register(generate_username, generate_password)

    def fin():
        user_db.delete_user(generate_username)
        auth_db.delete_by_username(generate_username)

    # request.addfinalizer(fin)
    return generate_username, generate_password

@pytest.fixture(scope="session")
def user(
        auth_client: OAuthClient,
        auth_db: AuthDB,
        user_db: UserDB,
        request: FixtureRequest,
        fake: Faker
) -> tuple[str, str]:
    username = fake.user_name()
    password = fake.password()
    auth_client.register(username, password)

    def fin():
        user_db.delete_user(username)
        auth_db.delete_by_username(username)

    # request.addfinalizer(fin)
    return username, password

@pytest.fixture
def user_without_spending(
        register_new_user: tuple[str, str],
        browser: Browser,
        login_page: LoginPage
):
    # context = browser.new_context()
    # page = context.new_page()
    # username, password = register_new_user
    # login_page.navigate()
    # login_page.fill_username(username)
    # login_page.fill_password(password)
    # login_page.submit()
    # yield page
    # context.close()
    #  todo
    username, password = register_new_user
    context = browser.new_context()
    page = context.new_page()

    login_page = LoginPage(page, server_cfg)
    login_page.navigate()
    login_page.fill_username(username)
    login_page.fill_password(password)
    login_page.submit()

    yield page  # или yield page, (username, password)

    context.close()

@pytest.fixture
def make_future_date() -> Callable[[int], str]:
    def _make(days: int) -> str:
        ft_date = datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=days)
        return ft_date.replace(hour=21, minute=0, second=0, microsecond=0).isoformat(timespec='milliseconds').replace('+00:00', 'Z')
    return _make