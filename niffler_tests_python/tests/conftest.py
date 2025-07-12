import datetime

import allure
import pytest
from typing import Callable
from collections.abc import Generator

from allure_commons.reporter import AllureReporter
from allure_pytest.listener import AllureListener
from pytest import Item, FixtureDef, FixtureRequest
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from niffler_tests_python.settings.client_config import ClientConfig
from niffler_tests_python.settings.server_config import ServerConfig
from niffler_tests_python.web_pages.LoginPage import LoginPage


pytest_plugins = [
    'niffler_tests_python.fixtures.auth_fixtures',
    'niffler_tests_python.fixtures.client_fixtures',
    'niffler_tests_python.fixtures.pages_fixtures',
    'niffler_tests_python.fixtures.category_fixtures',
    'niffler_tests_python.fixtures.spend_fixtures',
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

def pytest_addoption(parser) -> None:
    parser.addoption("--browser", default="chrome")

@pytest.fixture(scope="session")
def server_cfg(request: FixtureRequest) -> ServerConfig:
    return ServerConfig(
        browser_name=request.config.getoption('--browser'),
        _env_file=".env"
    )

@pytest.fixture(scope="session")
def client_cfg() -> ClientConfig:
    return ClientConfig(_env_file=".env")

@pytest.fixture
def username(client_cfg: ClientConfig) -> str:
    return client_cfg.username

@pytest.fixture(scope="session")
def browser(request: FixtureRequest) -> Generator[WebDriver, None, None]:
    browser_name = request.config.getoption('browser')
    browser = None
    if browser_name == 'chrome':
        browser = webdriver.Chrome()
    elif browser_name == 'firefox':
        options = FirefoxOptions()
        browser = webdriver.Firefox(options=options)

    browser.set_window_size(1280, 800)

    yield browser

    browser.quit()

@pytest.fixture(scope="session")
def auth_browser(browser: WebDriver, login_page: LoginPage, client_cfg: ClientConfig) -> WebDriver:
    login_page.open()
    login_page.enter_username(client_cfg.username)
    login_page.enter_password(client_cfg.password.get_secret_value())
    login_page.click_login_button()
    return browser

@pytest.fixture
def make_future_date() -> Callable[[int], str]:
    def _make(days: int) -> str:
        ft_date = datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=days)
        return ft_date.replace(hour=21, minute=0, second=0, microsecond=0).isoformat(timespec='milliseconds').replace('+00:00', 'Z')
    return _make
