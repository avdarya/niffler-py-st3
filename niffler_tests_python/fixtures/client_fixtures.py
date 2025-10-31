from typing import Generator, Any

import grpc
import pytest
from grpc import insecure_channel

from niffler_tests_python.clients.category_client import CategoryApiClient
from niffler_tests_python.clients.graphql_client import GraphQLClient
from niffler_tests_python.clients.kafka_client import KafkaClient
from niffler_tests_python.clients.spend_client import SpendApiClient
from niffler_tests_python.clients.user_client import UserApiClient
from niffler_tests_python.databases.auth_db import AuthDB
from niffler_tests_python.databases.friendship_db import FriendshipDB
from niffler_tests_python.databases.spend_db import SpendDB
from niffler_tests_python.databases.user_db import UserDB
from niffler_tests_python.grpc_pb.internal.grpc.interceptors.grpc_allure import GRPCAllureInterceptor
from niffler_tests_python.grpc_pb.internal.grpc.interceptors.grpc_logging import GRPCLoggingInterceptor
from niffler_tests_python.grpc_pb.internal.pb.niffler_currency_pb2_pbreflect import NifflerCurrencyServiceClient
from niffler_tests_python.settings.grpc_config import GRPCConfig
from niffler_tests_python.settings.server_config import ServerConfig
from niffler_tests_python.utils.sessions import BaseSession, SoapSession, GraphqlSession


@pytest.fixture
def base_session(
        server_cfg: ServerConfig,
        user: tuple[str, str],
        auth_token_factory
) -> BaseSession:
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
