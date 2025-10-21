import allure
from faker import Faker

from xmlschema import XMLSchemaChildrenValidationError

from niffler_tests_python.databases.user_db import UserDB
from niffler_tests_python.model.enums.currency_title import CurrencyTitle
from niffler_tests_python.model.enums.friendship_status import  FriendshipAPIStatus
from niffler_tests_python.templates.soap.read_templates import xml_current_user, xsd_response, xml_all_users_page
from niffler_tests_python.utils.sessions import SoapSession
from niffler_tests_python.utils.soap_parser import parsed_xml_user
from niffler_tests_python.utils.waiters import wait_until_timeout


@allure.epic("Пользователи")
@allure.feature("Текущий пользователь")
@allure.story("SOAP API")
@allure.tag("positive")
@allure.title("Получение данных текущего пользователя")
def test_get_current_user(
        soap_session: SoapSession,
        user: tuple[str, str],
        user_db: UserDB,
):
    username, _ = user
    with allure.step("Получаем данные пользователя из базы через DBClient"):
        user_from_db = wait_until_timeout(user_db.get_userdata_by_username)(username)
    with allure.step("Отправляем SOAP-запрос"):
        response = soap_session.request(method='POST', data=xml_current_user(username))
    with allure.step("Проверяем статус 200"):
        assert response.status_code == 200
    with allure.step("Валидируем XSD-схему userResponse"):
        try:
            xsd_response('userResponse').validate(response.text)
        except XMLSchemaChildrenValidationError as xsd_e:
            raise AssertionError(xsd_e)
    with allure.step("Сравниваем поля ответа и БД"):
        parsed_response = parsed_xml_user(response.text)
        assert parsed_response['id'] == str(user_from_db.id)
        assert parsed_response['username'] == username
        assert parsed_response['fullname'] == user_from_db.full_name
        assert parsed_response['currency'] == user_from_db.currency
        assert parsed_response['friendship'] == FriendshipAPIStatus.VOID


@allure.epic("Пользователи")
@allure.feature("Текущий пользователь")
@allure.story("SOAP API")
@allure.tag("negative")
@allure.title("Получение данных несуществующего пользователя")
def test_get_non_existing_user(
        soap_session: SoapSession,
        fake: Faker,
):
    username = fake.user_name()
    with allure.step("Отправляем SOAP-запрос для получения несуществующего пользователя"):
        response = soap_session.request(method='POST', data=xml_current_user(username))
    with allure.step("Проверяем статус ответа 200"):
        assert response.status_code == 200
    with allure.step("Проверяем, что ответ соответствует XSD-схеме userResponse"):
        try:
            xsd_response('userResponse').validate(response.text)
        except XMLSchemaChildrenValidationError as xsd_e:
            raise AssertionError(xsd_e)
    with allure.step("Парсим XML и проверяем значения по умолчанию"):
        parsed_response = parsed_xml_user(response.text)
        assert parsed_response['id'] is None
        assert parsed_response['username'] == username
        assert parsed_response['fullname'] is None
        assert parsed_response['currency'] == CurrencyTitle.RUB
        assert parsed_response['friendship'] == FriendshipAPIStatus.VOID