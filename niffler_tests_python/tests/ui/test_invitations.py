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





@Pages.go_to_people_all_after_people
def test_user_can_send_invitation(
        user: tuple[str, str],
        register_new_user: tuple[str, str],
        clean_up_friendships_for_users: list[UserModelDB],
        people_all_page: PeopleAllPage,
        user_client: UserApiClient,
        user_db: UserDB,
        friendship_db: FriendshipDB,
):
    current_username, _ = user
    people_name, _ = register_new_user

    people_row = people_all_page.get_people_row(people_name)
    people_all_page.click_add_friend(people_row)

    assert people_all_page.notification.get_notification_text() == f"Invitation sent to {people_name}"
    people_all_page.notification.is_success_notification()

    # TODO
    with allure.step('TODO'):
        people_all_page.expected_waiting_chip(people_row)

    requested_user = user_db.get_userdata_by_username(current_username)
    addressed_user = user_db.get_userdata_by_username(people_name)

    record_by_req_addr = friendship_db.get_friendship(requested_user.id, addressed_user.id)
    record_by_addr_req = friendship_db.get_friendship(addressed_user.id, requested_user.id)
    assert record_by_req_addr.status == FriendshipDBStatus.PENDING
    assert record_by_addr_req is None


    clean_up_friendships_for_users.append(requested_user)
    clean_up_friendships_for_users.append(addressed_user)

    api_users_all = user_client.get_users_all(search_query=addressed_user.username)
    content = api_users_all.get('content', [])
    assert len(content) == 1
    friend = UserFriendshipModel(**content[0])
    assert friend.username == people_name
    assert friend.id == str(addressed_user.id)
    assert friend.friendshipStatus == FriendshipAPIStatus.INVITE_SENT

@Pages.go_to_people_friends_after_send
def test_user_can_accept_invitation(
        user: tuple[str, str],
        register_new_user: tuple[str, str],
        people_friends_page: PeopleFriendsPage,
        user_client: UserApiClient,
        user_db: UserDB,
        friendship_db: FriendshipDB,
):
    current_username, _ = user
    requester_name, _ = register_new_user

    friend_row = people_friends_page.get_friend_row(requester_name)
    people_friends_page.click_accept(friend_row)
    assert people_friends_page.notification.get_notification_text() == f'Invitation of {requester_name} accepted'
    people_friends_page.notification.is_success_notification()
    people_friends_page.expected_unfriend_button(friend_row)

    requested_user = user_db.get_userdata_by_username(requester_name)
    addressed_user = user_db.get_userdata_by_username(current_username)

    record_by_req_addr = friendship_db.get_friendship(requested_user.id, addressed_user.id)
    record_by_addr_req = friendship_db.get_friendship(addressed_user.id, requested_user.id)
    assert record_by_req_addr.status == FriendshipDBStatus.ACCEPTED
    assert record_by_addr_req.status == FriendshipDBStatus.ACCEPTED

    #     clean_up_friendships_for_users.append(requested_user)
    #     clean_up_friendships_for_users.append(addressed_user)

    api_friends_all = user_client.get_friends_all(search_query=requester_name)
    content = api_friends_all.get('content', [])

    assert len(content) == 1
    friend = UserFriendshipModel(**content[0])
    assert friend.username == requester_name
    assert friend.id == str(requested_user.id)
    assert friend.friendshipStatus == FriendshipAPIStatus.FRIEND

@Pages.go_to_people_friends_after_send
def test_user_can_decline_invitation(
        user: tuple[str, str],
        register_new_user: tuple[str, str],
        people_friends_page: PeopleFriendsPage,
        user_client: UserApiClient,
        user_db: UserDB,
        friendship_db: FriendshipDB,
):
    current_username, _ = user
    requester_name, _ = register_new_user
    friend_row = people_friends_page.get_friend_row(requester_name)
    people_friends_page.click_decline(friend_row)
    people_friends_page.click_popup_decline_button()
    assert people_friends_page.notification.get_notification_text() == f'Invitation of {requester_name} is declined'
    people_friends_page.notification.is_success_notification()

    assert people_friends_page.get_friend_row(requester_name) is None

    requested_user = user_db.get_userdata_by_username(requester_name)
    addressed_user = user_db.get_userdata_by_username(current_username)

    record_by_req_addr = friendship_db.get_friendship(requested_user.id, addressed_user.id)
    record_by_addr_req = friendship_db.get_friendship(addressed_user.id, requested_user.id)
    assert record_by_req_addr is None
    assert record_by_addr_req is None

#     #     clean_up_friendships_for_users.append(requested_user)
#     #     clean_up_friendships_for_users.append(addressed_user)
#
    api_friends_all = user_client.get_friends_all(search_query=requester_name)
    assert len(api_friends_all['content']) == 0

@Pages.go_to_people_friends_after_accept
def test_user_can_delete_friend(
        user: tuple[str, str],
        register_new_user: tuple[str, str],
        people_friends_page: PeopleFriendsPage,
        user_client: UserApiClient,
        user_db: UserDB,
        friendship_db: FriendshipDB,
        accept_invitation: None
):
    current_username, _ = user
    requester_name, _ = register_new_user
    friend_row = people_friends_page.get_friend_row(requester_name)

    people_friends_page.click_unfriend(friend_row)
    people_friends_page.click_popup_delete_button()

    assert people_friends_page.notification.get_notification_text() == f'Friend {requester_name} is deleted'
    people_friends_page.notification.is_success_notification()

    assert people_friends_page.get_friend_row(requester_name) is None
#
    requested_user = user_db.get_userdata_by_username(requester_name)
    addressed_user = user_db.get_userdata_by_username(current_username)
    record_by_req_addr = friendship_db.get_friendship(requested_user.id, addressed_user.id)
    record_by_addr_req = friendship_db.get_friendship(addressed_user.id, requested_user.id)
    assert record_by_req_addr is None
    assert record_by_addr_req is None

    api_friends_all = user_client.get_friends_all(search_query=requester_name)
    assert len(api_friends_all['content']) == 0