from time import sleep

import allure
from faker import Faker

from niffler_tests_python.databases.auth_db import AuthDB
from niffler_tests_python.databases.user_db import UserDB
from niffler_tests_python.utils.waiters import wait_until_timeout
from niffler_tests_python.web_pages.LoginPage import LoginPage
from niffler_tests_python.web_pages.RegisterPage import RegisterPage


@allure.epic("Авторизация")
@allure.feature("Регистрация")
@allure.story("UI")
@allure.tag("positive")
@allure.title("Регистрация пользователя — запись в базы auth и userdata")
def test_register_success(
    register_page: RegisterPage,
    username_with_teardown: str,
    fake: Faker,
    auth_db: AuthDB,
    user_db: UserDB,
):
    password = fake.password()
    with allure.step("Открыть /register"):
        register_page.navigate()
    with allure.step("Заполнить форму регистрации"):
        register_page.fill_username(username_with_teardown)
        register_page.fill_password(password)
        register_page.fill_password_submit(password)
    with allure.step("Отправить форму"):
        register_page.submit()
    with allure.step("Проверить экран успеха"):
        register_page.is_show_success_message()
        register_page.is_show_success_signin_button()
    with allure.step("Дождаться записи в БД auth"):
        auth_user_from_db = wait_until_timeout(auth_db.get_by_username)(username_with_teardown)
        assert auth_user_from_db.username == username_with_teardown
    with allure.step("Дождаться записи в БД userdata"):
        user_from_db = wait_until_timeout(user_db.get_userdata_by_username)(username_with_teardown)
        assert user_from_db.username == username_with_teardown


@allure.epic("Авторизация")
@allure.feature("Регистрация")
@allure.story("UI")
@allure.tag("positive")
@allure.title("После регистрации кнопка 'Sign in' ведет на страницу входа /login")
def test_register_redirect_to_login(
    register_page: RegisterPage,
    login_page: LoginPage,
    username_with_teardown: str,
    fake: Faker,
):
    password = fake.password()
    with allure.step("Открыть /register"):
        register_page.navigate()
    with allure.step("Заполнить и отправить форму регистрации"):
        register_page.fill_username(username_with_teardown)
        register_page.fill_password(password)
        register_page.fill_password_submit(password)
        register_page.submit()
        sleep(2)
    with allure.step("Нажать на кнопку Sign in после успешной регистрации"):
        register_page.is_show_success_signin_button()
        register_page.click_success_signin()
        sleep(2)
    with allure.step("Проверить переход на страницу /login и отображение заголовка Log in"):
        login_page.expected_url()
        login_page.is_visible_login_text()
        sleep(2)