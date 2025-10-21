import allure
import pytest

from niffler_tests_python.clients.category_client import CategoryApiClient
from niffler_tests_python.databases.spend_db import SpendDB
from niffler_tests_python.utils.helpers import get_category_by_name


@allure.epic("Траты")
@allure.feature("Создание категории")
@allure.story("API")
@allure.tag("positive")
@allure.title("Пользователь может создать новую категорию")
@pytest.mark.parametrize("category_name", ["added category"])
def test_add_category_and_verify_data(
        category_client: CategoryApiClient,
        spend_db: SpendDB,
        category_name: str,
        user: tuple[str, str],
):
    username, _  = user

    with allure.step("Получить количество категорий до добавления"):
        before_category_count = len(category_client.get_all_categories())

    with allure.step("Добавить новую категорию через API"):
        added_category = category_client.add_category(category_name=category_name)

    with allure.step("Проверить, что категория появилась в списке через API"):
        api_category = get_category_by_name(category_name, category_client)

    with allure.step("Получить количество категорий после добавления"):
        after_category_count = len(category_client.get_all_categories())

    with allure.step("Проверить категорию в базе данных"):
        db_category = spend_db.get_category_by_id(added_category.id)

    with allure.step("Удалить тестовую категорию из базы"):
        spend_db.delete_category(db_category.id)

    with allure.step("Проверить корректность данных созданной категории"):
        assert added_category.name == category_name, "Имя созданной категории не совпадает с ожидаемым"
        assert added_category.archived is False, "Созданная категория помечена как архивная"
        assert added_category.username == username, "Имя пользователя созданной категории не совпадает с ожидаемым"

    with allure.step("Проверить корректность данных категории в API"):
        assert api_category.name == category_name, "Имя категории из API не совпадает с ожидаемым"
        assert api_category.archived is False, "Категория из API помечена как архивная"
        assert api_category.username == username, "Имя пользователя категории из API не совпадает с ожидаемым"
        assert before_category_count + 1 == after_category_count, "Количество категорий увеличилось на 1"

    with allure.step("Проверить корректность данных категории в базе данных"):
        assert db_category.name == category_name, "Имя категории из БД не совпадает с ожидаемым"
        assert db_category.archived is False, "Категория из БД помечена как архивная"
        assert db_category.username == username, "Имя пользователя категории из БД не совпадает с ожидаемым"
