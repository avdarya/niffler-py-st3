import allure
from faker import Faker

from niffler_tests_python.databases.auth_db import AuthDB
from niffler_tests_python.utils.waiters import wait_until_timeout
from niffler_tests_python.web_pages.RegisterPage import RegisterPage


@allure.epic("Авторизация")
@allure.feature("Регистрация")
@allure.story("UI")
@allure.tag("negative")
@allure.title("Регистрация пользователя с несовпадающими паролями")
def test_passwords_not_equal(
        register_page: RegisterPage,
        fake: Faker,
        auth_db: AuthDB,
):
    username = fake.user_name()
    password = fake.password()
    with allure.step("Открыть /register"):
        register_page.navigate()
    with allure.step("Заполнить поле username"):
        register_page.fill_username(username)
    with allure.step("Заполнить поля password, submit_password несовпадающими значениями"):
        register_page.fill_password(password)
        register_page.fill_password_submit(password[1:])
    with allure.step("Отправить форму"):
        register_page.submit()
    with allure.step("Проверить отображение сообщения: Пароли должны совпадать"):
        register_page.is_show_passwords_should_by_equal()
    with allure.step("Проверить отсутствие записи в БД auth"):
        auth_user_from_db = wait_until_timeout(auth_db.get_all_records_by_username)(username)
        assert len(auth_user_from_db) == 0