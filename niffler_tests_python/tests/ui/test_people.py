from time import sleep
from typing import Callable

import allure

from niffler_tests_python.clients.oauth_client import OAuthClient
from niffler_tests_python.clients.user_client import UserApiClient
from niffler_tests_python.databases.friendship_db import FriendshipDB
from niffler_tests_python.databases.user_db import UserDB
from niffler_tests_python.fixtures.people_fixtures import sending_invitation
from niffler_tests_python.model.enums.friendship_status import FriendshipDBStatus, FriendshipAPIStatus
from niffler_tests_python.model.userdata import UserModelDB, UserFriendshipModel, UserName
from niffler_tests_python.settings.server_config import ServerConfig
from niffler_tests_python.utils.marks import Pages, TestData
from niffler_tests_python.utils.sessions import BaseSession
from niffler_tests_python.web_pages.PeopleAllPage import PeopleAllPage
from niffler_tests_python.web_pages.PeopleFriendsPage import PeopleFriendsPage


@Pages.go_to_people_all_after_list_people
@TestData.people_list(15)
def test_people_list_viewing(
        people_list: list[UserModelDB],
        people_all_page: PeopleAllPage,
        user_client: UserApiClient,
):
    ui_usernames = people_all_page.get_all_usernames()

    api_response = user_client.get_users_all()
    api_people = [UserFriendshipModel(**p) for p in api_response.get("content", [])]

    ui_names = sorted(ui_usernames)
    api_names = sorted(p.username for p in api_people)
    assert len(api_names) == len(ui_usernames)
    assert ui_names == api_names

@Pages.go_to_people_friends_after_list_friend
@TestData.friend_list(15)
def test_friends_list_viewing(
        friend_list: list[UserModelDB],
        people_friends_page: PeopleFriendsPage,
        user_client: UserApiClient,
):
    ui_usernames = people_friends_page.get_all_usernames()

    api_response = user_client.get_friends_all()
    api_people = [UserFriendshipModel(**p) for p in api_response.get("content", [])]

    ui_names = sorted(ui_usernames)
    api_names = sorted(p.username for p in api_people)
    assert len(api_names) == len(ui_usernames)
    assert ui_names == api_names