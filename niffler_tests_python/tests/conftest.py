import allure
import grpc
import pytest
import os
import subprocess
from typing import Any
from collections.abc import Generator

from allure_commons.reporter import AllureReporter
from allure_pytest.listener import AllureListener
from faker import Faker
from pytest import Item, FixtureDef, FixtureRequest
from grpc import insecure_channel

from niffler_tests_python.grpc_pb.internal.grpc.interceptors.grpc_allure import GRPCAllureInterceptor
from niffler_tests_python.grpc_pb.internal.grpc.interceptors.grpc_logging import GRPCLoggingInterceptor
from niffler_tests_python.grpc_pb.internal.pb.niffler_currency_pb2_pbreflect import NifflerCurrencyServiceClient

from niffler_tests_python.clients.kafka_client import KafkaClient
from niffler_tests_python.settings.grpc_config import GRPCConfig
from niffler_tests_python.settings.server_config import ServerConfig

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

# for parallel tests -->
# def pytest_configure(config):
#     # объявляем маркеры (чтобы pytest 8 не ругался)
#     config.addinivalue_line("markers", "isolated: test must run serialized on a single worker")
#     config.addinivalue_line("markers", "xdist_group(name): group tests to the same xdist worker")
#
# def _xdist_active(config) -> bool:
#     # контролёр (не воркер) и действительно включён -n
#     return (
#         config.pluginmanager.hasplugin("xdist")
#         and getattr(config, "workerinput", None) is None
#         and getattr(config.option, "numprocesses", 0)
#     )
#
# def pytest_collection_modifyitems(config, items):
#     """
#     НИЧЕГО не выкидываем из коллекции.
#     Если запущено с -n, помечаем все @pytest.mark.isolated как xdist_group("__isolated__")
#     и принудительно переводим стратегию в loadgroup — тогда группа выполняется
#     ПOСЛЕДОВАТЕЛЬНО на одном воркере, остальные тесты параллелятся как обычно.
#     """
#     if _xdist_active(config):
#         # включаем режим распределения по группам
#         if getattr(config.option, "dist", None) != "loadgroup":
#             config.option.dist = "loadgroup"
#
#         for item in items:
#             if item.get_closest_marker("isolated"):
#                 item.add_marker(pytest.mark.xdist_group("__isolated__"))

####
# def pytest_sessionstart(session):
#     session.config._isolated_tests = []
#
# def pytest_collection_modifyitems(session, config, items):
#     isolated = [i for i in items if i.get_closest_marker("isolated")]
#     others = [i for i in items if i not in isolated]
#     session.config._isolated_tests = isolated
#     items[:] = others  # убираем изолированные из основного прохода
#
# def pytest_sessionfinish(session, exitstatus):
#     isolated = getattr(session.config, "_isolated_tests", [])
#     if isolated and not os.getenv("RUNNING_ISOLATED"):
#         env = os.environ.copy()
#         env["RUNNING_ISOLATED"] = "1"
#         cmd = ["pytest", "-m", "isolated", "-s", "-v"]
#         if session.config.option.numprocesses:
#             cmd.append("--maxfail=1")
#         subprocess.run(cmd, check=False, env=env)
#
# def pytest_deselected(items):
#     pass
#
# def pytest_report_collectionfinish(config, start_path, items):
#     return f"collected {len(items)} test items"
#  <-- for parallel test

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

    print(f'\nFROM conftest')
    print(f'\nFROM conftest')
    print(f'server_cfg.spend_db_url={config.spend_db_url}')
    print(f'server_cfg.userdata_db_url={config.userdata_db_url}')
    print(f'server_cfg.auth_db_url={config.auth_db_url}')

    print(f'server_cfg.frontend_url={config.frontend_url}')
    print(f'server_cfg.gateway_url={config.gateway_url}')
    print(f'server_cfg.auth_url={config.auth_url}')

    print(f'server_cfg.kafka_address={config.kafka_address}')
    print(f'server_cfg.soap_url={config.soap_url}')
    print(f'server_cfg.graphql_url={config.graphql_url}')

    return config

@pytest.fixture(scope="session")
def grpc_cfg(request: FixtureRequest) -> GRPCConfig:
    return GRPCConfig()

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
