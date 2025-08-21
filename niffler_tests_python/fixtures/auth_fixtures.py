import pytest

from niffler_tests_python.clients.oauth_client import OAuthClient
from niffler_tests_python.settings.client_config import ClientConfig
from niffler_tests_python.settings.server_config import ServerConfig


@pytest.fixture(scope="session")
def auth_client(server_cfg: ServerConfig) -> OAuthClient:
    return OAuthClient(server_cfg)

@pytest.fixture(scope="session")
def auth_token(auth_client: OAuthClient, client_cfg: ClientConfig) -> str:
    return auth_client.access_token(client_cfg.username, client_cfg.password.get_secret_value())

