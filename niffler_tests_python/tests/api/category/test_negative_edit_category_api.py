import allure
import pytest

from niffler_tests_python.clients.category_client import CategoryApiClient
from niffler_tests_python.databases.spend_db import SpendDB
from niffler_tests_python.model.category import CategoryModel
from niffler_tests_python.utils.helpers import get_category_by_name


@allure.epic("Траты")
@allure.feature("Редактирование категории")
@allure.story("API")
@allure.tag("negative")
@allure.title("Пользователь не может переименовать категорию, используя имя уже существующей категории")
@pytest.mark.parametrize("two_categories", [("category 1", "category 2")], indirect=True)
def test_change_category_name_for_existing_category(
        two_categories: tuple[CategoryModel, CategoryModel],
        category_client: CategoryApiClient,
        spend_db: SpendDB
):
    category_1, category_2 = two_categories

    with allure.step("Отправить запрос на изменение имени категории на уже существующее"):
        edited_category_1 = category_client.update_category_error(
            {
                "id": category_1.id,
                "name": category_2.name,
            }
        )

    with allure.step("Получить список категорий через API"):
        api_category_1 = get_category_by_name(category_1.name, category_client)

    with allure.step("Получить данные категории из базы данных"):
        db_category_1 = spend_db.get_category_by_id(category_1.id)

    with allure.step("Проверить, что имя категории не изменилось"):
        assert api_category_1.name == category_1.name
        assert db_category_1.name == category_1.name

    with allure.step("Проверить тело ответа об ошибке"):
        assert edited_category_1.type == "niffler-spend: Bad request "
        assert edited_category_1.title == "Conflict"
        assert edited_category_1.status == 409
        assert edited_category_1.detail == "Cannot save duplicates"
        assert edited_category_1.instance == "/api/categories/update"