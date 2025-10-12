from time import sleep
from typing import Callable, Generator

import pytest
from _pytest.fixtures import FixtureRequest
from faker import Faker

from niffler_tests_python.clients.oauth_client import OAuthClient
from niffler_tests_python.clients.user_client import UserApiClient
from niffler_tests_python.databases import friendship_db
from niffler_tests_python.databases.auth_db import AuthDB
from niffler_tests_python.databases.friendship_db import FriendshipDB
from niffler_tests_python.databases.user_db import UserDB
from niffler_tests_python.model.friendship import FriendshipModelDB
from niffler_tests_python.model.userdata import UserModelDB, UserName, UserFriendshipModel
from niffler_tests_python.settings.server_config import ServerConfig
from niffler_tests_python.utils.sessions import BaseSession


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
    base_session = BaseSession(gateway_url=server_cfg.gateway_url, token=token)
    rest_client = UserApiClient(base_session)
    rest_client.send_invitation(UserName(username=addressed_username))

    def fin():
        friendship_db.delete_by_requester_id(requested_username)

    # request.addfinalizer(fin)

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

    # request.addfinalizer(fin)

@pytest.fixture
def clean_up_friendships_for_users(friendship_db: FriendshipDB) -> Generator[list, UserModelDB, None]:
    users: list[UserModelDB] = []
    yield users
    for user in users:
        friendship_db.delete_by_requester_id(user.id)
        friendship_db.delete_by_addressee_id(user.id)

@pytest.fixture
def people_list(
        request: FixtureRequest,
        auth_client: OAuthClient,
        user_db: UserDB,
        auth_db: AuthDB,
        friendship_db: FriendshipDB,
        fake: Faker,
) -> list[UserModelDB]:
    count = request.param
    people_list: list[UserModelDB] = []

    for _ in range(count):
        username = fake.user_name()
        password = fake.password()
        auth_client.register(username, password)
        for _ in range(5):
            db_user = user_db.get_userdata_by_username(username)
            if db_user:
                break
            sleep(0.5)
        else:
            raise RuntimeError(f"User {username} not found in DB after registration")

        people_list.append(db_user)

    def fin():
        for user in people_list:
            friendship_db.delete_by_requester_id(user.id)
            friendship_db.delete_by_addressee_id(user.id)
            user_db.delete_user(user.username)
            auth_db.delete_by_username(user.username)

    request.addfinalizer(fin)
    return people_list

@pytest.fixture
def friend_list(
        fake: Faker,
        request: FixtureRequest,
        server_cfg: ServerConfig,
        auth_client: OAuthClient,
        user_client: UserApiClient,
        user: tuple[str, str],
        friendship_db: FriendshipDB,
        user_db: UserDB,
        auth_db: AuthDB,
) -> list[UserModelDB]:
    addressed_username, _ = user
    count = request.param
    friend_list: list[UserModelDB] = []

    for _ in range(count):
        username = fake.user_name()
        password = fake.password()
        auth_client.register(username, password)
        for _ in range(5):
            db_user = user_db.get_userdata_by_username(username)
            if db_user:
                break
            sleep(0.5)
        else:
            raise RuntimeError(f"User {username} not found in DB after registration")

        friend_list.append(db_user)

        token = auth_client.access_token(username, password)
        base_session = BaseSession(gateway_url=server_cfg.gateway_url, token=token)
        rest_client = UserApiClient(base_session)
        rest_client.send_invitation(UserName(username=addressed_username))
        user_client.accept_invitation(UserName(username=username))

    def fin():
        for user in friend_list:
            friendship_db.delete_by_requester_id(user.id)
            friendship_db.delete_by_addressee_id(user.id)
            user_db.delete_user(user.username)
            auth_db.delete_by_username(user.username)

    request.addfinalizer(fin)
    return friend_list