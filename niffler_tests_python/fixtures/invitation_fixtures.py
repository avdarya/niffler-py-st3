from typing import Generator

import pytest
from _pytest.fixtures import FixtureRequest

from niffler_tests_python.clients.oauth_client import OAuthClient
from niffler_tests_python.clients.user_client import UserApiClient
from niffler_tests_python.databases.friendship_db import FriendshipDB
from niffler_tests_python.databases.user_db import UserDB
from niffler_tests_python.model.userdata import UserModelDB, UserName
from niffler_tests_python.settings.server_config import ServerConfig
from niffler_tests_python.utils.sessions import BaseSession


@pytest.fixture
def clean_up_friendships_for_users(friendship_db: FriendshipDB) -> Generator[list, UserModelDB, None]:
    users: list[UserModelDB] = []
    yield users
    for user in users:
        friendship_db.delete_by_requester_id(user.id)
        friendship_db.delete_by_addressee_id(user.id)


@pytest.fixture
def accept_invitation(
        sending_invitation: None,
        register_new_user: tuple[str, str],
        user: tuple[str, str],
        request: FixtureRequest,
        user_db: UserDB,
        friendship_db: FriendshipDB,
        user_client: UserApiClient,
):
    addressed_user = user_db.get_userdata_by_username(user[0])
    requested_user = user_db.get_userdata_by_username(register_new_user[0])

    user_client.accept_invitation(UserName(username=requested_user.username))
    def fin():
        friendship_db.delete_by_requester_id(addressed_user.id)
        friendship_db.delete_by_addressee_id(addressed_user.id)

    request.addfinalizer(fin)


@pytest.fixture
def sending_invitation(
        server_cfg: ServerConfig,
        auth_client: OAuthClient,
        register_new_user: tuple[str, str],
        user: tuple[str, str],
        friendship_db: FriendshipDB,
        request: FixtureRequest,
        user_db: UserDB,
) -> None:
    addressed_username, _ = user
    requested_username, password = register_new_user
    token = auth_client.access_token(requested_username, password)
    local_session = BaseSession(gateway_url=server_cfg.gateway_url, token=token)
    rest_client = UserApiClient(local_session)
    rest_client.send_invitation(UserName(username=addressed_username))

    def fin():
        requester_user = user_db.get_userdata_by_username(requested_username)
        addresser_user = user_db.get_userdata_by_username(addressed_username)
        friendship_db.delete_by_requester_id(requester_user.id)
        friendship_db.delete_by_requester_id(addresser_user.id)

    request.addfinalizer(fin)
