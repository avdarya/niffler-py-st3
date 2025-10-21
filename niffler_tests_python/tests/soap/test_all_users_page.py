import allure
from math import ceil

import pytest
from xmlschema import XMLSchemaChildrenValidationError

from niffler_tests_python.databases.user_db import UserDB
from niffler_tests_python.model.userdata import UserModelDB
from niffler_tests_python.templates.soap.read_templates import  xsd_response, xml_all_users_page
from niffler_tests_python.utils.marks import TestData
from niffler_tests_python.utils.sessions import SoapSession
from niffler_tests_python.utils.soap_parser import parsed_xml_users_page


@allure.epic("Пользователи")
@allure.feature("Просмотр списка пользователей")
@allure.story("SOAP API")
@allure.tag("positive")
@allure.title("Получение страницы со списком пользователей")
@pytest.mark.parametrize('page, size', [(0, 10), (1, 10)])
@TestData.people_list(15)
def test_get_all_users_page(
        soap_session: SoapSession,
        user: tuple[str, str],
        people_list: list[UserModelDB],
        user_db: UserDB,
        page: int,
        size: int,
):
    username, _ = user
    with allure.step("Отправляем SOAP-запрос на получение страницы пользователей"):
        response = soap_session.request(method='POST', data=xml_all_users_page(
            username=username,
            page=page,
            size=size,
            search_query=''
        ))
    assert response.status_code == 200
    with allure.step("Проверяем, что ответ соответствует XSD-схеме"):
        try:
            xsd_response('usersResponse').validate(response.text)
        except XMLSchemaChildrenValidationError as xsd_e:
            raise AssertionError(xsd_e)
    with allure.step("Парсим XML-ответ и извлекаем пользователей"):
        parsed_response = parsed_xml_users_page(response.text)
        api_usernames = [user['username'] for user in parsed_response['users']]
    with allure.step("Получаем пользователей из базы данных"):
        db_users = user_db.get_users_by_filter(page=page, size=size, sort='username')
        db_usernames = [user.username for user in db_users]
        db_total_people = user_db.get_users_count() - 1
    with allure.step("Проверяем соответствие пользователей API ↔ БД"):
        assert len(api_usernames) == len(db_usernames)
        assert set(api_usernames) == set(db_usernames)
        assert parsed_response['size'] == size
        assert parsed_response['number'] == page
        assert parsed_response['totalElements'] == db_total_people
        assert parsed_response['totalPages'] == ceil(db_total_people / size)

@allure.epic("Пользователи")
@allure.feature("Поиск пользователей")
@allure.story("SOAP API")
@allure.tag("positive")
@allure.title("Получение страницы пользователей по поисковому запросу")
@pytest.mark.parametrize('page, size', [(0, 10)])
@TestData.people_list(15)
def test_get_all_users_page_by_search(
        soap_session: SoapSession,
        user: tuple[str, str],
        people_list: list[UserModelDB],
        register_new_user: tuple[str, str],
        user_db: UserDB,
        page: int,
        size: int,
):
    username, _ = user
    searched_username, _ = register_new_user
    with allure.step("Отправляем SOAP-запрос на получение страницы пользователей по поисковому параметру"):
        response = soap_session.request(method='POST', data=xml_all_users_page(
            username=username,
            page=page,
            size=size,
            search_query=searched_username
        ))
    assert response.status_code == 200
    with allure.step("Проверяем, что ответ соответствует XSD-схеме"):
        try:
            xsd_response('usersResponse').validate(response.text)
        except XMLSchemaChildrenValidationError as xsd_e:
            raise AssertionError(xsd_e)
    with allure.step("Парсим XML-ответ и извлекаем пользователей"):
        parsed_response = parsed_xml_users_page(response.text)
        api_usernames = [user['username'] for user in parsed_response['users']]
    with allure.step("Получаем пользователей из базы данных по поисковому запросу"):
        db_users = user_db.get_users_by_filter(page=page, size=size, sort='username', search_query=searched_username)
        db_usernames = [user.username for user in db_users]
        db_total_people = user_db.get_users_count(search_query=searched_username)
    with allure.step("Проверяем соответствие результатов поиска API ↔ БД"):
        assert len(api_usernames) == len(db_usernames)
        assert set(api_usernames) == set(db_usernames)
        assert parsed_response['size'] == size
        assert parsed_response['number'] == page
        assert parsed_response['totalElements'] == db_total_people
        assert parsed_response['totalPages'] == ceil(db_total_people / size)
