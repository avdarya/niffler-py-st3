import allure
from math import ceil

import pytest
from xmlschema import XMLSchemaChildrenValidationError

from niffler_tests_python.databases.friendship_db import FriendshipDB
from niffler_tests_python.databases.user_db import UserDB
from niffler_tests_python.model.db_model.userdata_db import UserModelDB
from niffler_tests_python.templates.soap.read_templates import  xsd_response, xml_friends_page
from niffler_tests_python.utils.marks import TestData
from niffler_tests_python.utils.sessions import SoapSession
from niffler_tests_python.utils.soap_parser import  parsed_xml_users_page


@allure.epic("Друзья")
@allure.feature("Получение списка друзей")
@allure.story("SOAP API")
@allure.tag("positive")
@allure.title("Пользователь может получить страницу со списком друзей")
@pytest.mark.isolated
@pytest.mark.parametrize('page, size', [(0, 10), (1, 10)])
@TestData.friend_list(15)
def test_get_friends_page(
        soap_session: SoapSession,
        user: tuple[str, str],
        friend_list: list[UserModelDB],
        friendship_db: FriendshipDB,
        user_db: UserDB,
        page: int,
        size: int,
):
    username, _ = user
    with allure.step("Отправляем SOAP-запрос на получение страницы друзей"):
        response = soap_session.request(method='POST', data=xml_friends_page(
            username=username,
            page=page,
            size=size,
            search_query=''
        ))
    with allure.step("Проверяем, что ответ имеет статус 200"):
        assert response.status_code == 200
    with allure.step("Валидируем XML по XSD-схеме usersResponse"):
        try:
            xsd_response('usersResponse').validate(response.text)
        except XMLSchemaChildrenValidationError as xsd_e:
            raise AssertionError(xsd_e)
    with allure.step("Парсим XML-ответ и извлекаем имена друзей"):
        parsed_response = parsed_xml_users_page(response.text)
        api_friend_names = [friend['username'] for friend in parsed_response['users']]
    with allure.step("Получаем список друзей из базы данных через DBClient"):
        user_id = user_db.get_userdata_by_username(username).id
        db_friends = friendship_db.get_friends_by_filter(user_id=user_id, page=page, size=size, sort='username')
        db_friend_names = [friend.username for friend in db_friends]
        db_total_friends = friendship_db.get_friends_count(user_id=user_id)
    with allure.step("Сравниваем данные API и БД"):
        assert len(api_friend_names) == len(db_friend_names)
        assert api_friend_names == db_friend_names
        assert parsed_response['size'] == size
        assert parsed_response['number'] == page
        assert parsed_response['totalElements'] == db_total_friends
        assert parsed_response['totalPages'] == ceil(db_total_friends / size)

@allure.epic("Друзья")
@allure.feature("Поиск друзей")
@allure.story("SOAP API")
@allure.tag("positive")
@allure.title("Пользователь может искать друзей по имени")
@pytest.mark.parametrize('page, size', [(0, 10)])
@TestData.friend_list(15)
def test_get_friends_page_by_search(
        soap_session: SoapSession,
        user: tuple[str, str],
        register_new_user: tuple[str, str],
        accept_invitation: None,
        friend_list: list[UserModelDB],
        friendship_db: FriendshipDB,
        user_db: UserDB,
        page: int,
        size: int,
):
    username, _ = user
    searched_username, _ = register_new_user
    with allure.step("Отправляем SOAP-запрос с поисковым параметром"):
        response = soap_session.request(method='POST', data=xml_friends_page(
            username=username,
            page=page,
            size=size,
            search_query=searched_username
        ))
    with allure.step("Проверяем статус ответа"):
        assert response.status_code == 200
    with allure.step("Валидируем XSD"):
        try:
            xsd_response('usersResponse').validate(response.text)
        except XMLSchemaChildrenValidationError as xsd_e:
            raise AssertionError(xsd_e)
    with allure.step("Парсим XML и извлекаем найденных друзей"):
        parsed_response = parsed_xml_users_page(response.text)
        api_friend_names = [friend['username'] for friend in parsed_response['users']]
    with allure.step("Сравниваем результаты поиска API и БД"):
        user_id = user_db.get_userdata_by_username(username).id
        db_friends = friendship_db.get_friends_by_filter(user_id=user_id, page=page, size=size, sort='username', search_query=searched_username)
        db_friend_names = [friend.username for friend in db_friends]
        db_total_friends = friendship_db.get_friends_count(user_id=user_id, search_query=searched_username)
        assert len(api_friend_names) == len(db_friend_names)
        assert api_friend_names == db_friend_names
        assert parsed_response['size'] == size
        assert parsed_response['number'] == page
        assert parsed_response['totalElements'] == db_total_friends
        assert parsed_response['totalPages'] == ceil(db_total_friends / size)
