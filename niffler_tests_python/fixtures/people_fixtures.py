import pytest
from _pytest.fixtures import FixtureRequest
from faker import Faker

from niffler_tests_python.clients.oauth_client import OAuthClient
from niffler_tests_python.clients.user_client import UserApiClient
from niffler_tests_python.databases.auth_db import AuthDB
from niffler_tests_python.databases.friendship_db import FriendshipDB
from niffler_tests_python.databases.user_db import UserDB
from niffler_tests_python.model.rest_model.userdata import UserName
from niffler_tests_python.model.db_model.userdata_db import UserModelDB
from niffler_tests_python.settings.server_config import ServerConfig
from niffler_tests_python.utils.sessions import BaseSession
from niffler_tests_python.utils.waiters import wait_until_timeout


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
        db_user = wait_until_timeout(user_db.get_userdata_by_username)(username)
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
        db_user = wait_until_timeout(user_db.get_userdata_by_username)(username)
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