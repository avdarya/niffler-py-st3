import pytest

from niffler_tests_python.clients.oauth_client import OAuthClient
from niffler_tests_python.settings.client_config import ClientConfig
from niffler_tests_python.settings.server_config import ServerConfig


@pytest.fixture(scope="session")
def auth_client(server_cfg: ServerConfig) -> OAuthClient:
    return OAuthClient(server_cfg)

# @pytest.fixture
# def auth_token(auth_client: OAuthClient, username: str, password: str) -> str:
#     return auth_client.access_token(username, password)


@pytest.fixture(scope="session")
def auth_token_factory(auth_client: OAuthClient):
    def _make(username: str, password: str) -> str:
        return auth_client.access_token(username, password)
    return _make

# @pytest.fixture
# def token(server_cfg: ServerConfig, username: str, password: str) -> str:
#     auth_client = OAuthClient(server_cfg)
#     return auth_client.access_token(username, password)