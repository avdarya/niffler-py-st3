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
from niffler_tests_python.templates.soap.read_templates import xsd_response, xml_send_invitation, xml_accept_invitation, \
    xml_decline_invitation, xml_remove_friend, xsd_error_response
from niffler_tests_python.utils.marks import TestData
from niffler_tests_python.utils.sessions import SoapSession
from niffler_tests_python.utils.soap_parser import parsed_xml_user, parsed_xml_fault
from niffler_tests_python.utils.waiters import wait_until_timeout


def test_send_invitation(
        soap_session: SoapSession,
        user: tuple[str, str],
        register_new_user: tuple[str, str],
        clean_up_friendships_for_users: list[UserModelDB],
        friendship_db: FriendshipDB,
        user_db: UserDB
):
    current_username, _ = user
    people_name, _ = register_new_user

    response = soap_session.request(method='POST', data=xml_send_invitation(
        username=current_username,
        addressed_username=people_name,
    ))
    assert response.status_code == 200
    try:
        xsd_response('userResponse').validate(response.text)
    except XMLSchemaChildrenValidationError as xsd_e:
        raise AssertionError(xsd_e)
    parsed_response = parsed_xml_user(response.text)

    db_friend = user_db.get_userdata_by_username(people_name)
    user = user_db.get_userdata_by_username(current_username)
    db_friendship = friendship_db.get_friendship(user.id, db_friend.id)

    clean_up_friendships_for_users.append(db_friend)

    assert parsed_response['id'] == str(db_friend.id)
    assert parsed_response['username'] == people_name
    assert parsed_response['fullname'] == db_friend.full_name
    assert parsed_response['currency'] == db_friend.currency
    assert parsed_response['friendship'] == FriendshipAPIStatus.INVITE_SENT
    assert db_friendship.status == FriendshipDBStatus.PENDING

def test_accept_invitation(
        soap_session: SoapSession,
        user: tuple[str, str],
        register_new_user: tuple[str, str],
        sending_invitation: None,
        clean_up_friendships_for_users: list[UserModelDB],
        friendship_db: FriendshipDB,
        user_db: UserDB
):
    current_username, _ = user
    requester_name, _ = register_new_user

    response = soap_session.request(method='POST', data=xml_accept_invitation(
        username=current_username,
        addressed_username=requester_name,
    ))
    assert response.status_code == 200
    try:
        xsd_response('userResponse').validate(response.text)
    except XMLSchemaChildrenValidationError as xsd_e:
        raise AssertionError(xsd_e)
    parsed_response = parsed_xml_user(response.text)

    db_friend = user_db.get_userdata_by_username(requester_name)
    user = user_db.get_userdata_by_username(current_username)

    record_by_req_addr = friendship_db.get_friendship(user.id, db_friend.id)
    record_by_addr_req = friendship_db.get_friendship(db_friend.id, user.id)

    assert parsed_response['id'] == str(db_friend.id)
    assert parsed_response['username'] == requester_name
    assert parsed_response['fullname'] == db_friend.full_name
    assert parsed_response['currency'] == db_friend.currency
    assert parsed_response['friendship'] == FriendshipAPIStatus.FRIEND
    assert record_by_req_addr.status == FriendshipDBStatus.ACCEPTED
    assert record_by_addr_req.status == FriendshipDBStatus.ACCEPTED

def test_decline_invitation(
        soap_session: SoapSession,
        user: tuple[str, str],
        register_new_user: tuple[str, str],
        sending_invitation: None,
        clean_up_friendships_for_users: list[UserModelDB],
        friendship_db: FriendshipDB,
        user_db: UserDB
):
    current_username, _ = user
    requester_name, _ = register_new_user

    response = soap_session.request(method='POST', data=xml_decline_invitation(
        username=current_username,
        addressed_username=requester_name,
    ))
    assert response.status_code == 200
    try:
        xsd_response('userResponse').validate(response.text)
    except XMLSchemaChildrenValidationError as xsd_e:
        raise AssertionError(xsd_e)
    parsed_response = parsed_xml_user(response.text)

    db_friend = user_db.get_userdata_by_username(requester_name)
    user = user_db.get_userdata_by_username(current_username)

    record_by_req_addr = friendship_db.get_friendship(user.id, db_friend.id)
    record_by_addr_req = friendship_db.get_friendship(db_friend.id, user.id)

    assert parsed_response['id'] == str(db_friend.id)
    assert parsed_response['username'] == requester_name
    assert parsed_response['fullname'] == db_friend.full_name
    assert parsed_response['currency'] == db_friend.currency
    assert parsed_response['friendship'] == FriendshipAPIStatus.VOID
    assert record_by_req_addr is None
    assert record_by_addr_req is None

def test_remove_friend(
        soap_session: SoapSession,
        user: tuple[str, str],
        register_new_user: tuple[str, str],
        accept_invitation: None,
        clean_up_friendships_for_users: list[UserModelDB],
        friendship_db: FriendshipDB,
        user_db: UserDB
):
    current_username, _ = user
    requester_name, _ = register_new_user

    response = soap_session.request(method='POST', data=xml_remove_friend(
        username=current_username,
        addressed_username=requester_name,
    ))
    assert response.status_code == 202
    assert response.text.strip() == ''

    db_friend = user_db.get_userdata_by_username(requester_name)
    user = user_db.get_userdata_by_username(current_username)

    record_by_req_addr = friendship_db.get_friendship(user.id, db_friend.id)
    record_by_addr_req = friendship_db.get_friendship(db_friend.id, user.id)

    assert record_by_req_addr is None
    assert record_by_addr_req is None

@pytest.mark.parametrize('expected_code, expected_text', [
    ('SOAP-ENV:Server', 'Can`t create friendship request for self user')
])
def test_self_send_invitation(
        soap_session: SoapSession,
        user: tuple[str, str],
        friendship_db: FriendshipDB,
        user_db: UserDB,
        expected_code,
        expected_text
):
    current_username, _ = user

    response = soap_session.request(method='POST', data=xml_send_invitation(
        username=current_username,
        addressed_username=current_username,
    ))

    assert response.status_code == 500
    try:
        xsd_error_response().validate(response.text)
    except XMLSchemaChildrenValidationError as e:
        raise AssertionError(f'Invalid SOAP Fault structure: {e}')

    parsed_response = parsed_xml_fault(response.text)

    assert parsed_response['faultcode'] == expected_code
    assert parsed_response['faultstring'] == expected_text

    user = user_db.get_userdata_by_username(current_username)
    db_friendship = friendship_db.get_friendship(user.id, user.id)

    assert db_friendship is None

@pytest.mark.parametrize('expected_code, expected_text', [
    ('SOAP-ENV:Server', 'Cannot invoke "java.util.List.size()" because "this.this$0.operationQueue" is null')
])
def test_send_duplicate_send_invitation(
        soap_session: SoapSession,
        user: tuple[str, str],
        register_new_user: tuple[str, str],
        sending_invitation: None,
        friendship_db: FriendshipDB,
        user_db: UserDB,
        expected_code,
        expected_text
):
    current_username, _ = user
    requester_name, _ = register_new_user

    response = soap_session.request(method='POST', data=xml_send_invitation(
        username=requester_name,
        addressed_username=current_username,
    ))

    assert response.status_code == 500
    try:
        xsd_error_response().validate(response.text)
    except XMLSchemaChildrenValidationError as e:
        raise AssertionError(f'Invalid SOAP Fault structure: {e}')

    parsed_response = parsed_xml_fault(response.text)

    assert parsed_response['faultcode'] == expected_code
    assert parsed_response['faultstring'] == expected_text

    db_friend = user_db.get_userdata_by_username(requester_name)
    user = user_db.get_userdata_by_username(current_username)
    db_friendship = friendship_db.get_friendship(db_friend.id, user.id)

    assert db_friendship.status == FriendshipDBStatus.PENDING

@pytest.mark.parametrize('expected_code, expected_text', [
    ('SOAP-ENV:Server', 'Can`t find invitation from username: ')
])
def test_accept_non_existing_invitation(
        soap_session: SoapSession,
        user: tuple[str, str],
        register_new_user: tuple[str, str],
        friendship_db: FriendshipDB,
        user_db: UserDB,
        expected_code,
        expected_text
):
    current_username, _ = user
    requester_name, _ = register_new_user

    response = soap_session.request(method='POST', data=xml_accept_invitation(
        username=current_username,
        addressed_username=requester_name,
    ))

    assert response.status_code == 500
    try:
        xsd_error_response().validate(response.text)
    except XMLSchemaChildrenValidationError as e:
        raise AssertionError(f'Invalid SOAP Fault structure: {e}')

    parsed_response = parsed_xml_fault(response.text)

    assert parsed_response['faultcode'] == expected_code
    assert parsed_response['faultstring'] == f"{expected_text}'{requester_name}'"

    db_friend = user_db.get_userdata_by_username(requester_name)
    user = user_db.get_userdata_by_username(current_username)
    db_friendship = friendship_db.get_friendship(user.id, db_friend.id)

    assert db_friendship is None


