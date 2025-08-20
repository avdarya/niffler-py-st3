import pytest

from niffler_tests_python.clients.oauth_client import OAuthClient
from niffler_tests_python.settings.client_config import ClientConfig
from niffler_tests_python.settings.server_config import ServerConfig


@pytest.fixture(scope="session")
def auth_token(server_cfg: ServerConfig, client_cfg: ClientConfig) -> str:
    return OAuthClient(server_cfg).access_token(client_cfg.username, client_cfg.password.get_secret_value())