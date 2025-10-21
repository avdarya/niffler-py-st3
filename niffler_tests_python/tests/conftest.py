import datetime
import uuid
import allure
import grpc
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
from grpc import insecure_channel

from niffler_tests_python.grpc_pb.internal.grpc.interceptors.grpc_allure import GRPCAllureInterceptor
from niffler_tests_python.grpc_pb.internal.grpc.interceptors.grpc_logging import GRPCLoggingInterceptor
from niffler_tests_python.grpc_pb.internal.pb.niffler_currency_pb2_pbreflect import NifflerCurrencyServiceClient

from niffler_tests_python.clients.kafka_client import KafkaClient
from niffler_tests_python.clients.oauth_client import OAuthClient
from niffler_tests_python.databases.auth_db import AuthDB
from niffler_tests_python.settings.grpc_config import GRPCConfig
from niffler_tests_python.settings.server_config import ServerConfig
from niffler_tests_python.web_pages.LoginPage import LoginPage
from niffler_tests_python.web_pages.RegisterPage import RegisterPage

pytest_plugins = [
    'niffler_tests_python.fixtures.auth_fixtures',
    'niffler_tests_python.fixtures.client_fixtures',
    'niffler_tests_python.fixtures.pages_fixtures',
    'niffler_tests_python.fixtures.category_fixtures',
    'niffler_tests_python.fixtures.spend_fixtures',
    'niffler_tests_python.fixtures.test_data_fixtures',
    'niffler_tests_python.fixtures.browser_fixtures',
    'niffler_tests_python.fixtures.people_fixtures',
    'niffler_tests_python.fixtures.invitation_fixtures',
]


def allure_logger(config) -> AllureReporter:
    listener: AllureListener = config.pluginmanager.get_plugin("allure_listener")
    return listener.allure_logger

def pytest_collection_modifyitems(items: list[Item]):
    for item in items:
        usefixtures_args = []
        for marker in item.iter_markers(name='usefixtures'):
            usefixtures_args.extend(marker.args)
        if usefixtures_args:
            item._fixture_tags = set(usefixtures_args)

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_setup(item: Item):
    for fx_name in getattr(item, '_fixture_tags', []):
        allure.dynamic.tag(f'@pytest.mark.usefixtures({fx_name})')
    yield

@pytest.hookimpl(hookwrapper=True, trylast=True)
def pytest_runtest_call(item: Item):
    yield
    allure.dynamic.title(" ".join(item.name.split("_")[1:]).title())

    logger = allure_logger(item.config)
    test_result = logger.get_last_item()
    if test_result:
        test_result.labels = [
            lbl
            for lbl in test_result.labels
            if not (lbl.name == "tag" and "usefixtures" in lbl.value)
        ]

@pytest.hookimpl(hookwrapper=True, trylast=True)
def pytest_fixture_setup(fixturedef: FixtureDef, request: FixtureRequest):
    yield
    logger = allure_logger(request.config)
    item = logger.get_last_item()
    scope_letter = fixturedef.scope[0].upper()
    item.name = f"[{scope_letter}] " + " ".join(fixturedef.argname.split("_")).title()

def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption('--grpc-mock', action='store_true', default=False)

@pytest.fixture(scope='session')
def fake() -> Faker:
    return Faker()

@pytest.fixture(scope="session")
def server_cfg(request: FixtureRequest) -> ServerConfig:
    raw = request.config.getoption('--browser')
    if isinstance(raw, (list, tuple)):
        chosen = raw[0] if raw else 'chromium'
    else:
        chosen = raw or 'chromium'
    config  = ServerConfig(
        browser_name=str(chosen).lower(),
        _env_file=".env"
    )
    print(f'\nFROM conftest server_cfg: config.frontend_url={config.frontend_url}\nconfig.auth_url={config.auth_url}\nconfig.auth_db_url={config.auth_db_url}')
    return config

@pytest.fixture(scope="session")
def grpc_cfg(request: FixtureRequest) -> GRPCConfig:
    return GRPCConfig(_env_file=".env")

# @pytest.fixture(scope="session")
# def client_cfg(auth_client: OAuthClient, register_new_user) -> ClientConfig:
#     username, password = register_new_user
#     return ClientConfig(
#         username=username,
#         password=SecretStr(password),
#     )

# @pytest.fixture
# def username(client_cfg: ClientConfig) -> str:
#     return client_cfg.username

# @pytest.fixture(scope="session")
# def browser(request: FixtureRequest) -> Generator[WebDriver, None, None]:
#     browser_name = request.config.getoption('browser')
#     browser = None
#     if browser_name == 'chrome':
#         browser = webdriver.Chrome()
#     elif browser_name == 'firefox':
#         options = FirefoxOptions()
#         browser = webdriver.Firefox(options=options)
#
#     browser.set_window_size(1280, 800)
#
#     yield browser
#
#     browser.quit()

# @pytest.fixture(scope="session")
# def auth_browser(browser: WebDriver, login_page: LoginPage, client_cfg: ClientConfig) -> WebDriver:
#     login_page.open()
#     login_page.enter_username(client_cfg.username)
#     login_page.enter_password(client_cfg.password.get_secret_value())
#     login_page.click_login_button()
#     return browser



@pytest.fixture(scope='session')
def kafka(server_cfg: ServerConfig) -> Generator[KafkaClient, Any, None]:
    with KafkaClient(server_cfg) as k:
        yield k

INTERCEPTORS = [
    GRPCLoggingInterceptor(),
    GRPCAllureInterceptor(),
]

@pytest.fixture(scope='session')
def grpc_client(grpc_cfg: GRPCConfig, request: pytest.FixtureRequest) -> NifflerCurrencyServiceClient:
    host = grpc_cfg.currency_service_host
    if request.config.getoption('--grpc-mock'):
        host = grpc_cfg.currency_wiremock_host
    channel = insecure_channel(host)
    intercepted_channel = grpc.intercept_channel(
        channel,
        *INTERCEPTORS
    )
    return NifflerCurrencyServiceClient(intercepted_channel)
