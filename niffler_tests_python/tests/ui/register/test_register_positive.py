import allure

from niffler_tests_python.databases.auth_db import AuthDB
from niffler_tests_python.databases.userdata_db import UserdataDB
from niffler_tests_python.utils.waiters import wait_until_timeout
from niffler_tests_python.web_pages.LoginPage import LoginPage
from niffler_tests_python.web_pages.RegisterPage import RegisterPage


@allure.epic("Auth")
@allure.feature("Registration")
@allure.story("Positive")
@allure.title("Регистрация пользователя → запись в auth БД и userdata БД")
def test_register_e2e(
    register_page: RegisterPage,
    user_with_teardown: str,
    generate_password: str,
    auth_db: AuthDB,
    userdata_db: UserdataDB,
):
    with allure.step("Открыть /register"):
        register_page.navigate()
    with allure.step("Заполнить форму регистрации"):
        register_page.fill_username(user_with_teardown)
        register_page.fill_password(generate_password)
        register_page.fill_password_submit(generate_password)
    with allure.step("Отправить форму"):
        register_page.submit()
    with allure.step("Проверить экран успеха"):
        register_page.is_show_success_message()
        register_page.is_show_success_signin_button()
    with allure.step("Дождаться записи в БД auth"):
        auth_user_from_db = wait_until_timeout(auth_db.get_by_username)(user_with_teardown)
        assert auth_user_from_db.username == user_with_teardown
    with allure.step("Дождаться записи в БД userdata"):
        user_from_db = wait_until_timeout(userdata_db.get_userdata_by_username)(user_with_teardown)
        assert user_from_db.username == user_with_teardown

@allure.epic("Auth")
@allure.feature("Registration")
@allure.story("Positive")
@allure.title("После успешной регистрации кнопка Sign in ведет на страницу /login")
def test_register_redirect_to_login(
    register_page: RegisterPage,
    login_page: LoginPage,
    user_with_teardown: str,
    generate_password: str
):
    with allure.step("Открыть /register"):
        register_page.navigate()
    with allure.step("Заполнить и отправить форму регистрации"):
        register_page.fill_username(user_with_teardown)
        register_page.fill_password(generate_password)
        register_page.fill_password_submit(generate_password)
        register_page.submit()
    with allure.step("Нажать на кнопку Sign in после успешной регистрации"):
        register_page.is_show_success_signin_button()
        register_page.click_success_signin()
    with allure.step("Проверить переход на страницу /login и отображение заголовка Log in"):
        login_page.is_correct_url()
        login_page.is_visible_login_text()