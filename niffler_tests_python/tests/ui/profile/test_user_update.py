import allure
import pytest
from niffler_tests_python.clients.user_client import UserApiClient
from niffler_tests_python.databases.user_db import UserDB
from niffler_tests_python.utils.marks import Pages
from niffler_tests_python.web_pages.ProfilePage import ProfilePage


@allure.epic("Профиль пользователя")
@allure.feature("Обновление данных пользователя")
@allure.story("UI")
@allure.tag("positive")
@allure.title("Пользователь может обновить свои данные через UI и проверить изменения в API и БД")
@Pages.go_to_profile_page
@pytest.mark.parametrize("fullname", ["Alex", "Mike"])
def  test_update_name(
        profile_page: ProfilePage,
        user_client: UserApiClient,
        user_db: UserDB,
        fullname
):
    with allure.step("Очищаем поле имени и вводим новое имя"):
        profile_page.clear_fullname_input()
        profile_page.enter_fullname(fullname)

    with allure.step("Сохраняем изменения профиля"):
        profile_page.click_save_changes()

    with allure.step("Получаем уведомление об успешном обновлении"):
        assert profile_page.notification.get_notification_text() == 'Profile successfully updated'
        profile_page.notification.is_success_notification()

    with allure.step("Получаем обновлённые данные пользователя через API"):
        api_user = user_client.get_current_user()

    with allure.step("Получаем обновлённые данные пользователя из БД"):
        db_userdata = user_db.get_userdata_by_username(api_user.username)

    with allure.step("Проверяем корректность обновления данных"):
        with allure.step("Проверяем имя пользователя в API"):
            assert fullname == api_user.fullname
        with allure.step("Проверяем имя пользователя в БД"):
            assert db_userdata.full_name == fullname
