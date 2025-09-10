import pytest

from niffler_tests_python.clients.category_client import CategoryApiClient
from niffler_tests_python.clients.spend_client import SpendApiClient
from niffler_tests_python.clients.user_client import UserApiClient
from niffler_tests_python.databases.auth_db import AuthDB
from niffler_tests_python.databases.spend_db import SpendDB
from niffler_tests_python.databases.userdata_db import UserdataDB
from niffler_tests_python.settings.server_config import ServerConfig
from niffler_tests_python.utils.sessions import BaseSession


@pytest.fixture(scope="session")
def base_session(server_cfg: ServerConfig, auth_token: str) -> BaseSession:
    return BaseSession(gateway_url=server_cfg.gateway_url, token=auth_token)

@pytest.fixture(scope="session")
def user_client(base_session: BaseSession) -> UserApiClient:
    return UserApiClient(session=base_session)

@pytest.fixture(scope="session")
def category_client(base_session: BaseSession) -> CategoryApiClient:
    return CategoryApiClient(session=base_session)

@pytest.fixture(scope="session")
def spend_client(base_session: BaseSession) -> SpendApiClient:
    return SpendApiClient(session=base_session)

@pytest.fixture(scope="session")
def spend_db(server_cfg: ServerConfig) -> SpendDB:
    return SpendDB(server_cfg)

@pytest.fixture(scope="session")
def userdata_db(server_cfg: ServerConfig) -> UserdataDB:
    return UserdataDB(server_cfg)

@pytest.fixture(scope="session")
def auth_db(server_cfg: ServerConfig) -> AuthDB:
    return AuthDB(server_cfg)