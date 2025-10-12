from math import ceil
from pathlib import Path
from time import sleep

import pytest
from xmlschema import XMLSchemaChildrenValidationError

from niffler_tests_python.databases.friendship_db import FriendshipDB
from niffler_tests_python.databases.user_db import UserDB
from niffler_tests_python.model.enums.currency_title import CurrencyTitle
from niffler_tests_python.model.enums.friendship_status import FriendshipDBStatus, FriendshipAPIStatus
from niffler_tests_python.model.userdata import UserModelDB
from niffler_tests_python.templates.soap.read_templates import xml_current_user, xsd_response, xml_all_users_page, \
    xml_friends_page
from niffler_tests_python.utils.marks import TestData
from niffler_tests_python.utils.sessions import SoapSession
from niffler_tests_python.utils.soap_parser import parsed_xml_user, parsed_xml_users_page
from niffler_tests_python.utils.waiters import wait_until_timeout


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
    response = soap_session.request(method='POST', data=xml_friends_page(
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
    api_friend_names = [friend['username'] for friend in parsed_response['users']]

    user_id = user_db.get_userdata_by_username(username).id
    db_friends = friendship_db.get_friends_by_filter(user_id=user_id, page=page, size=size, sort='username')
    db_friend_names = [friend.username for friend in db_friends]
    db_total_friends = friendship_db.get_friends_count(user_id=user_id)

    assert len(api_friend_names) == len(db_friend_names)
    assert api_friend_names == db_friend_names
    assert parsed_response['size'] == size
    assert parsed_response['number'] == page
    assert parsed_response['totalElements'] == db_total_friends
    assert parsed_response['totalPages'] == ceil(db_total_friends / size)

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
    response = soap_session.request(method='POST', data=xml_friends_page(
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
    api_friend_names = [friend['username'] for friend in parsed_response['users']]

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
