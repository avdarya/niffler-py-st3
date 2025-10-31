import pytest
from faker import Faker
from pytest import FixtureRequest
from niffler_tests_python.clients.oauth_client import OAuthClient
from niffler_tests_python.databases.auth_db import AuthDB
from niffler_tests_python.databases.user_db import UserDB


@pytest.fixture
def user(
        auth_client: OAuthClient,
        auth_db: AuthDB,
        user_db: UserDB,
        request: FixtureRequest,
        fake: Faker,
        worker_id: str
) -> tuple[str, str]:
    username = f'{fake.user_name()}_{worker_id}'
    password = fake.password()
    auth_client.register(username, password)

    def fin():
        user_db.delete_user(username)
        auth_db.delete_by_username(username)

    request.addfinalizer(fin)
    return username, password

@pytest.fixture
def username_with_teardown(
        auth_db: AuthDB,
        user_db: UserDB,
        request: FixtureRequest,
        fake: Faker,
        worker_id: str
) -> str:
    username = f'{fake.user_name()}_{worker_id}'

    def fin():
        user_db.delete_user(username)
        auth_db.delete_by_username(username)

    request.addfinalizer(fin)
    return username

@pytest.fixture
def register_new_user(
        auth_client: OAuthClient,
        auth_db: AuthDB,
        user_db: UserDB,
        request: FixtureRequest,
        fake: Faker,
        worker_id: str
) -> tuple[str, str]:
    username = f'{fake.user_name()}_{worker_id}'
    password = fake.password()
    auth_client.register(username, password)
    def fin():
        user_db.delete_user(username)
        auth_db.delete_by_username(username)

    request.addfinalizer(fin)
    return username, password

@pytest.fixture
def cleanup_user(auth_db, user_db, request):
    usernames: list[str] = []
    def add_username(name: str):
        usernames.append(name)
    yield add_username
    for username in usernames:
        user_db.delete_user(username)
        auth_db.delete_by_username(username)