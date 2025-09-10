import allure

from niffler_tests_python.web_pages.LoginPage import LoginPage


@allure.epic("Auth")
@allure.feature("Authorization")
@allure.story("Negative")
@allure.title("Авторизация пользователя с неверным паролем")
def test_login_wrong_password(
        registered_user: tuple[str, str],
        login_page: LoginPage
):
    username, password = registered_user
    with allure.step("Открыть /login"):
        login_page.navigate()
    with allure.step("Заполнить форму авторизации"):
        login_page.fill_username(username)
        login_page.fill_password(password[1:])
    with allure.step("Отправить форму с неверным паролем"):
        login_page.submit()
    with allure.step("Проверить, что пользователь на странице /login?error"):
        login_page.is_correct_error_url()
    with allure.step("Проверить, что отображается сообщение о неверных данных пользователя"):
        login_page.is_visible_wrong_user_data_text()
