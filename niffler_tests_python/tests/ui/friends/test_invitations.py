import allure

from niffler_tests_python.clients.user_client import UserApiClient
from niffler_tests_python.databases.friendship_db import FriendshipDB
from niffler_tests_python.databases.user_db import UserDB
from niffler_tests_python.model.enums.friendship_status import FriendshipDBStatus, FriendshipAPIStatus
from niffler_tests_python.model.userdata import UserModelDB, UserFriendshipModel
from niffler_tests_python.utils.marks import Pages
from niffler_tests_python.web_pages.PeopleAllPage import PeopleAllPage
from niffler_tests_python.web_pages.PeopleFriendsPage import PeopleFriendsPage





@allure.epic("Друзья")
@allure.feature("Отправка приглашения")
@allure.story("UI")
@allure.tag("positive")
@allure.title("Пользователь может отправить приглашение в друзья")
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

    with allure.step("Открываем страницу 'Все пользователи' и отправляем приглашение в друзья"):
        people_row = people_all_page.get_people_row(people_name)
        people_all_page.click_add_friend(people_row)

    with allure.step("Проверяем уведомление об успешной отправке приглашения"):
        assert people_all_page.notification.get_notification_text() == f"Invitation sent to {people_name}"
        people_all_page.notification.is_success_notification()

    with allure.step("Проверяем наличие метки ожидания у пользователя"):
        people_all_page.expected_waiting_chip(people_row)

    with allure.step("Проверяем запись о дружбе в БД"):
        requested_user = user_db.get_userdata_by_username(current_username)
        addressed_user = user_db.get_userdata_by_username(people_name)
        record_by_req_addr = friendship_db.get_friendship(requested_user.id, addressed_user.id)
        record_by_addr_req = friendship_db.get_friendship(addressed_user.id, requested_user.id)
        assert record_by_req_addr.status == FriendshipDBStatus.PENDING
        assert record_by_addr_req is None
        clean_up_friendships_for_users.append(requested_user)
        clean_up_friendships_for_users.append(addressed_user)

    with allure.step("Проверяем статус дружбы через API"):
        api_users_all = user_client.get_users_all(search_query=addressed_user.username)
        content = api_users_all.get('content', [])
        assert len(content) == 1
        friend = UserFriendshipModel(**content[0])
        assert friend.username == people_name
        assert friend.id == str(addressed_user.id)
        assert friend.friendshipStatus == FriendshipAPIStatus.INVITE_SENT

@allure.epic("Друзья")
@allure.feature("Принятие приглашения")
@allure.story("UI")
@allure.tag("positive")
@allure.title("Пользователь может принять приглашение в друзья")
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

    with allure.step("Принимаем приглашение на странице друзей"):
        friend_row = people_friends_page.get_friend_row(requester_name)
        people_friends_page.click_accept(friend_row)

    with allure.step("Проверяем уведомление об успешном принятии приглашения"):
        assert people_friends_page.notification.get_notification_text() == f'Invitation of {requester_name} accepted'
        people_friends_page.notification.is_success_notification()
        people_friends_page.expected_unfriend_button(friend_row)

    with allure.step("Проверяем изменения в БД"):
        requested_user = user_db.get_userdata_by_username(requester_name)
        addressed_user = user_db.get_userdata_by_username(current_username)
        record_by_req_addr = friendship_db.get_friendship(requested_user.id, addressed_user.id)
        record_by_addr_req = friendship_db.get_friendship(addressed_user.id, requested_user.id)
        assert record_by_req_addr.status == FriendshipDBStatus.ACCEPTED
        assert record_by_addr_req.status == FriendshipDBStatus.ACCEPTED

    with allure.step("Проверяем статус дружбы через API"):
        api_friends_all = user_client.get_friends_all(search_query=requester_name)
        content = api_friends_all.get('content', [])
        assert len(content) == 1
        friend = UserFriendshipModel(**content[0])
        assert friend.username == requester_name
        assert friend.id == str(requested_user.id)
        assert friend.friendshipStatus == FriendshipAPIStatus.FRIEND

@allure.epic("Друзья")
@allure.feature("Отклонение приглашения")
@allure.story("UI")
@allure.tag("positive")
@allure.title("Пользователь может отклонить приглашение в друзья")
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
    with allure.step("Отклоняем приглашение в друзья"):
        friend_row = people_friends_page.get_friend_row(requester_name)
        people_friends_page.click_decline(friend_row)
        people_friends_page.click_popup_decline_button()

    with allure.step("Проверяем уведомление об успешном отклонении приглашения"):
        assert people_friends_page.notification.get_notification_text() == f'Invitation of {requester_name} is declined'
        people_friends_page.notification.is_success_notification()

    with allure.step("Проверяем, что пользователь исчез из списка друзей и запись удалена из БД"):
        assert people_friends_page.get_friend_row(requester_name) is None
        requested_user = user_db.get_userdata_by_username(requester_name)
        addressed_user = user_db.get_userdata_by_username(current_username)
        record_by_req_addr = friendship_db.get_friendship(requested_user.id, addressed_user.id)
        record_by_addr_req = friendship_db.get_friendship(addressed_user.id, requested_user.id)
        assert record_by_req_addr is None
        assert record_by_addr_req is None

    with allure.step("Проверяем отсутствие записей через API"):
        api_friends_all = user_client.get_friends_all(search_query=requester_name)
        assert len(api_friends_all['content']) == 0

@allure.epic("Друзья")
@allure.feature("Удаление друга")
@allure.story("UI")
@allure.tag("positive")
@allure.title("Пользователь может удалить друга из списка")
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
    with allure.step("Удаляем друга со страницы друзей"):
        friend_row = people_friends_page.get_friend_row(requester_name)
        people_friends_page.click_unfriend(friend_row)
        people_friends_page.click_popup_delete_button()

    with allure.step("Проверяем уведомление об успешном удалении друга"):
        assert people_friends_page.notification.get_notification_text() == f'Friend {requester_name} is deleted'
        people_friends_page.notification.is_success_notification()

    with allure.step("Проверяем, что друг удалён из списка и из БД"):
        assert people_friends_page.get_friend_row(requester_name) is None
        requested_user = user_db.get_userdata_by_username(requester_name)
        addressed_user = user_db.get_userdata_by_username(current_username)
        record_by_req_addr = friendship_db.get_friendship(requested_user.id, addressed_user.id)
        record_by_addr_req = friendship_db.get_friendship(addressed_user.id, requested_user.id)
        assert record_by_req_addr is None
        assert record_by_addr_req is None

    with allure.step("Проверяем отсутствие друга через API"):
        api_friends_all = user_client.get_friends_all(search_query=requester_name)
        assert len(api_friends_all['content']) == 0