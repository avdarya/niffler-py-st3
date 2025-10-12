from math import ceil
from pathlib import Path
from time import sleep

import pytest
from xmlschema import XMLSchemaChildrenValidationError

from niffler_tests_python.databases.user_db import UserDB
from niffler_tests_python.model.enums.currency_title import CurrencyTitle
from niffler_tests_python.model.enums.friendship_status import FriendshipDBStatus, FriendshipAPIStatus
from niffler_tests_python.model.userdata import UserModelDB
from niffler_tests_python.templates.soap.read_templates import xml_current_user, xsd_response, xml_all_users_page
from niffler_tests_python.utils.marks import TestData
from niffler_tests_python.utils.sessions import SoapSession
from niffler_tests_python.utils.soap_parser import parsed_xml_user, parsed_xml_users_page
from niffler_tests_python.utils.waiters import wait_until_timeout


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
    response = soap_session.request(method='POST', data=xml_all_users_page(
        username=username,
        page=page,
        size=size,
        search_query=''
    ))
    assert response.status_code == 200
    try:
        xsd_response('usersResponse').validate(response.text)
    except XMLSchemaChildrenValidationError as xsd_e:
        raise AssertionError(xsd_e)
    parsed_response = parsed_xml_users_page(response.text)
    api_usernames = [user['username'] for user in parsed_response['users']]

    db_users = user_db.get_users_by_filter(page=page, size=size, sort='username')
    db_usernames = [user.username for user in db_users]
    db_total_people = user_db.get_users_count() - 1

    assert len(api_usernames) == len(db_usernames)
    assert api_usernames == db_usernames
    assert parsed_response['size'] == size
    assert parsed_response['number'] == page
    assert parsed_response['totalElements'] == db_total_people
    assert parsed_response['totalPages'] == ceil(db_total_people / size)

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
    response = soap_session.request(method='POST', data=xml_all_users_page(
        username=username,
        page=page,
        size=size,
        search_query=searched_username
    ))
    assert response.status_code == 200
    try:
        xsd_response('usersResponse').validate(response.text)
    except XMLSchemaChildrenValidationError as xsd_e:
        raise AssertionError(xsd_e)
    parsed_response = parsed_xml_users_page(response.text)
    api_usernames = [user['username'] for user in parsed_response['users']]

    db_users = user_db.get_users_by_filter(page=page, size=size, sort='username', search_query=searched_username)
    db_usernames = [user.username for user in db_users]
    db_total_people = user_db.get_users_count(search_query=searched_username)

    assert len(api_usernames) == len(db_usernames)
    assert api_usernames == db_usernames
    assert parsed_response['size'] == size
    assert parsed_response['number'] == page
    assert parsed_response['totalElements'] == db_total_people
    assert parsed_response['totalPages'] == ceil(db_total_people / size)
