import allure
import pytest

from niffler_tests_python.clients.user_client import UserApiClient
from niffler_tests_python.model.rest_model.userdata import UserFriendshipModel
from niffler_tests_python.model.db_model.userdata_db import UserModelDB
from niffler_tests_python.utils.marks import Pages, TestData
from niffler_tests_python.web_pages.PeopleAllPage import PeopleAllPage
from niffler_tests_python.web_pages.PeopleFriendsPage import PeopleFriendsPage


@allure.epic("Авторизация")
@allure.feature("Просмотр списка пользователей")
@allure.story("UI")
@allure.tag("positive")
@allure.title("Проверка отображения списка пользователей на странице 'Люди'")
@Pages.go_to_people_all_after_list_people
@TestData.people_list(15)
@pytest.mark.isolated
def test_people_list_viewing(
        people_list: list[UserModelDB],
        people_all_page: PeopleAllPage,
        user_client: UserApiClient,
):
    with allure.step("Открываем страницу 'Все пользователи' и получаем список имён с UI"):
        ui_usernames = people_all_page.get_all_usernames()

    with allure.step("Получаем список пользователей через API"):
        api_response = user_client.get_users_all()
        api_people = [UserFriendshipModel(**p) for p in api_response.get("content", [])]

    with allure.step("Сравниваем количество пользователей и их имена"):
        ui_names = sorted(ui_usernames)
        api_names = sorted(p.username for p in api_people)
        assert len(api_names) == len(ui_usernames)
        assert set(ui_names) == set(api_names)

@allure.epic("Авторизация")
@allure.feature("Просмотр списка друзей")
@allure.story("UI")
@allure.tag("positive")
@allure.title("Проверка отображения списка друзей на странице 'Друзья'")
@Pages.go_to_people_friends_after_list_friend
@TestData.friend_list(15)
@pytest.mark.isolated
def test_friends_list_viewing(
        friend_list: list[UserModelDB],
        people_friends_page: PeopleFriendsPage,
        user_client: UserApiClient,
):
    with allure.step("Открываем страницу 'Друзья' и получаем список имён с UI"):
        ui_usernames = people_friends_page.get_all_usernames()

    with allure.step("Получаем список друзей через API"):
        api_response = user_client.get_friends_all()
        api_people = [UserFriendshipModel(**p) for p in api_response.get("content", [])]

    with allure.step("Сравниваем количество друзей и их имена"):
        ui_names = sorted(ui_usernames)
        api_names = sorted(p.username for p in api_people)
        assert len(api_names) == len(ui_usernames)
        assert set(ui_names) == set(api_names)