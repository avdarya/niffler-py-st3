import allure
import pytest

from allure_commons.reporter import AllureReporter
from allure_pytest.listener import AllureListener
from faker import Faker
from pytest import Item, FixtureDef, FixtureRequest

from niffler_tests_python.settings.grpc_config import GRPCConfig
from niffler_tests_python.settings.server_config import ServerConfig

pytest_plugins = [
    'niffler_tests_python.fixtures.auth_fixtures',
    'niffler_tests_python.fixtures.client_fixtures',
    'niffler_tests_python.fixtures.pages_fixtures',
    'niffler_tests_python.fixtures.category_fixtures',
    'niffler_tests_python.fixtures.spend_fixtures',
    'niffler_tests_python.fixtures.user_fixtures',
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
    logger = allure_logger(item.config)
    test_result = logger.get_last_item()

    if test_result and not test_result.name:
        allure.dynamic.title(" ".join(item.name.split("_")[1:]).title())

    if test_result:
        test_result.labels = [
            lbl for lbl in test_result.labels
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
        browser_name=str(chosen).lower()
    )
    return config

@pytest.fixture(scope="session")
def grpc_cfg(request: FixtureRequest) -> GRPCConfig:
    return GRPCConfig()
