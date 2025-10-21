import pytest

from niffler_tests_python.clients.category_client import CategoryApiClient
from niffler_tests_python.clients.graphql_client import GraphQLClient
from niffler_tests_python.clients.spend_client import SpendApiClient
from niffler_tests_python.clients.user_client import UserApiClient
from niffler_tests_python.databases.auth_db import AuthDB
from niffler_tests_python.databases.friendship_db import FriendshipDB
from niffler_tests_python.databases.spend_db import SpendDB
from niffler_tests_python.databases.user_db import UserDB
from niffler_tests_python.settings.server_config import ServerConfig
from niffler_tests_python.utils.sessions import BaseSession, SoapSession, GraphqlSession


@pytest.fixture
def base_session(
        server_cfg: ServerConfig,
        user: tuple[str, str],
        auth_token_factory
) -> BaseSession:
    print(f'\nFROM client fixuters base session: \nserver_cfg.frontend_url={server_cfg.frontend_url} \nusernsme={user[0]}')
    username, password = user
    token = auth_token_factory(username, password)
    return BaseSession(gateway_url=server_cfg.gateway_url, token=token)

@pytest.fixture(scope="session")
def soap_session(server_cfg: ServerConfig) -> SoapSession:
    return SoapSession(soap_url=server_cfg.soap_url)

@pytest.fixture
def graphql_session(
        server_cfg: ServerConfig,
        user: tuple[str, str],
        auth_token_factory
) -> GraphqlSession:
    username, password = user
    token = auth_token_factory(username, password)
    return GraphqlSession(graphql_url=server_cfg.graphql_url, token=token)

@pytest.fixture
def user_client(base_session: BaseSession) -> UserApiClient:
    client = UserApiClient(session=base_session)
    return client

@pytest.fixture
def category_client(base_session: BaseSession) -> CategoryApiClient:
    return CategoryApiClient(session=base_session)

@pytest.fixture
def spend_client(base_session: BaseSession) -> SpendApiClient:
    return SpendApiClient(session=base_session)

@pytest.fixture
def graphql_client(graphql_session: GraphqlSession) -> GraphQLClient:
    return GraphQLClient(session=graphql_session)

@pytest.fixture(scope="session")
def spend_db(server_cfg: ServerConfig) -> SpendDB:
    return SpendDB(server_cfg)

@pytest.fixture(scope="session")
def user_db(server_cfg: ServerConfig) -> UserDB:
    return UserDB(server_cfg)

@pytest.fixture(scope="session")
def friendship_db(server_cfg: ServerConfig) -> FriendshipDB:
    return FriendshipDB(server_cfg)

@pytest.fixture(scope="session")
def auth_db(server_cfg: ServerConfig) -> AuthDB:
    return AuthDB(server_cfg)