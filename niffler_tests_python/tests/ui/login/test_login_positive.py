import allure

from niffler_tests_python.utils.helpers import decode_jwt_payload
from niffler_tests_python.web_pages.LoginPage import LoginPage
from niffler_tests_python.web_pages.MainPage import MainPage
from niffler_tests_python.web_pages.RegisterPage import RegisterPage


@allure.epic("Auth")
@allure.feature("Authorization")
@allure.story("Positive")
@allure.title("Авторизация пользователя -> переход /main")
def test_login_success(
        registered_user: tuple[str, str],
        login_page: LoginPage,
        main_page_guest: MainPage
):
    username, password = registered_user
    with allure.step("Открыть /login"):
        login_page.navigate()
    with allure.step("Заполнить форму авторизации"):
        login_page.fill_username(username)
        login_page.fill_password(password)
    with allure.step("Отправить форму"):
        login_page.submit()
    with allure.step("Проверить переход на страницу /main"):
        main_page_guest.is_correct_url()
        main_page_guest.is_visible_person_icon()
    with allure.step("Проверить в localStorage сохранены токены"):
        has_access_token = main_page_guest._page.evaluate("() => !!localStorage.getItem('access_token')")
        has_id_token = main_page_guest._page.evaluate("() => !!localStorage.getItem('id_token')")
        assert has_access_token and has_id_token
    with allure.step("Проверить имя пользователя в access_token"):
        access_token = main_page_guest._page.evaluate('() => localStorage.getItem("access_token")')
        header_b64, payload_b64, _sig = access_token.split('.')
        decoded_jwt_payload = decode_jwt_payload(payload_b64)
        assert decoded_jwt_payload.get('sub') == username

@allure.epic("Auth")
@allure.feature("Authorization")
@allure.story("Positive")
@allure.title("Переход /login -> /register по кнопке 'Create new account")
def test_navigate_from_login_to_register_page(login_page: LoginPage, register_page: RegisterPage):
    with allure.step("Открыть /login"):
        login_page.navigate()
    with allure.step("Нажать на кнопку создать новый аккаунт"):
        login_page.click_create_new_account()
    with allure.step("Проверить переход на страницу /register и отображение заголовка Sign up"):
        register_page.is_correct_url()
        register_page.is_visible_signup_text()
