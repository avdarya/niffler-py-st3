import allure
import pytest

from niffler_tests_python.clients.category_client import CategoryApiClient
from niffler_tests_python.databases.spend_db import SpendDB
from niffler_tests_python.utils.marks import Pages
from niffler_tests_python.utils.helpers import get_category_by_name
from niffler_tests_python.web_pages.ProfilePage import ProfilePage


@allure.epic("Траты")
@allure.feature("Создание категории")
@allure.story("UI")
@allure.tag("positive")
@allure.title("Добавление новой категории через интерфейс")
@Pages.go_to_profile_page
@pytest.mark.parametrize("category_name", ["added category"])
def test_add_category(
        user: tuple[str, str],
        profile_page: ProfilePage,
        category_client: CategoryApiClient,
        spend_db: SpendDB,
        category_name: str
):
    with allure.step("Открываем страницу профиля и вводим название новой категории"):
        profile_page.enter_add_category(category_name)

    with allure.step("Проверяем уведомление об успешном добавлении категории"):
        profile_page.notification.is_success_notification()
        assert f"You've added new category: {category_name}" == profile_page.notification.get_notification_text()

    with allure.step("Проверяем, что категория создана через API"):
        api_category = get_category_by_name(category_name, category_client)

    with allure.step("Проверяем добавленную категорию в базе данных"):
        db_category = spend_db.get_user_category_by_name(username=user[0], name=category_name)

    with allure.step("Удаляем тестовую категорию из базы данных"):
        spend_db.delete_category(db_category.id)

    with allure.step("Проверяем корректность данных категории во всех слоях системы"):
        with allure.step("Категория из API не в архиве"):
            assert api_category.archived is False
        with allure.step("Поле ввода очищено после добавления категории"):
            profile_page.expected_add_input_empty()
        with allure.step("Категория отображается в UI"):
            profile_page.expected_active_category_chip(category_name)
        with allure.step("Название категории в базе совпадает с введённым"):
            assert db_category.name == category_name
        with allure.step("Категория в базе не заархивирована"):
            assert db_category.archived is False