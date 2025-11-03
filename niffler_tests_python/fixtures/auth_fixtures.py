import pytest

from niffler_tests_python.clients.oauth_client import OAuthClient
from niffler_tests_python.settings.server_config import ServerConfig


@pytest.fixture
def auth_client(server_cfg: ServerConfig) -> OAuthClient:
    return OAuthClient(server_cfg)

@pytest.fixture
def auth_token_factory(server_cfg: ServerConfig):
    def _make(username: str, password: str) -> str:
        client = OAuthClient(server_cfg)
        return client.access_token(username, password)
    return _make
