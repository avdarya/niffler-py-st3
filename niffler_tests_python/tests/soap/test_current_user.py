from pathlib import Path
from time import sleep

import pytest
from xmlschema import XMLSchemaChildrenValidationError

from niffler_tests_python.databases.user_db import UserDB
from niffler_tests_python.model.enums.currency_title import CurrencyTitle
from niffler_tests_python.model.enums.friendship_status import FriendshipDBStatus, FriendshipAPIStatus
from niffler_tests_python.model.userdata import UserModelDB
from niffler_tests_python.templates.soap.read_templates import xml_current_user, xsd_response, xml_all_users_page
from niffler_tests_python.utils.sessions import SoapSession
from niffler_tests_python.utils.soap_parser import parsed_xml_user
from niffler_tests_python.utils.waiters import wait_until_timeout


def test_get_current_user(
        soap_session: SoapSession,
        user: tuple[str, str],
        user_db: UserDB,
):
    username, _ = user
    user_from_db = wait_until_timeout(user_db.get_userdata_by_username)(username)
    response = soap_session.request(method='POST', data=xml_current_user(username))
    assert response.status_code == 200
    try:
        xsd_response('userResponse').validate(response.text)
    except XMLSchemaChildrenValidationError as xsd_e:
        raise AssertionError(xsd_e)
    parsed_response = parsed_xml_user(response.text)
    assert parsed_response['id'] == str(user_from_db.id)
    assert parsed_response['username'] == username
    assert parsed_response['fullname'] == user_from_db.full_name
    assert parsed_response['currency'] == user_from_db.currency
    assert parsed_response['friendship'] == FriendshipAPIStatus.VOID

def test_get_non_existing_user(
        soap_session: SoapSession,
        generate_username: str,
):
    response = soap_session.request(method='POST', data=xml_current_user(generate_username))
    assert response.status_code == 200
    try:
        xsd_response('userResponse').validate(response.text)
    except XMLSchemaChildrenValidationError as xsd_e:
        raise AssertionError(xsd_e)
    parsed_response = parsed_xml_user(response.text)
    assert parsed_response['id'] is None
    assert parsed_response['username'] == generate_username
    assert parsed_response['fullname'] is None
    assert parsed_response['currency'] == CurrencyTitle.RUB
    assert parsed_response['friendship'] == FriendshipAPIStatus.VOID