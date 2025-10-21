import allure
import pytest

from niffler_tests_python.clients.category_client import CategoryApiClient
from niffler_tests_python.databases.spend_db import SpendDB
from niffler_tests_python.model.category import CategoryModel
from niffler_tests_python.utils.marks import TestData


@allure.epic("Траты")
@allure.feature("Создание категории")
@allure.story("API")
@allure.tag("negative")
@allure.title("Пользователь не может создать больше 8 категорий")
@TestData.fill_categories
@pytest.mark.parametrize("category_name", ["excess category"])
def test_add_over_category(
        category_name: str,
        category_client: CategoryApiClient,
        user: tuple[str, str],
        spend_db: SpendDB
):
   username, _ = user
   with allure.step("Получить количество категорий до добавления"):
      before_get_all_categories = category_client.get_all_categories()
      before_category_count = len(before_get_all_categories)

   with allure.step("Отправить запрос на добавление категории"):
      excess_category = category_client.add_category_error({"name": category_name})

   with allure.step("Получить количество категорий после добавления"):
      after_get_all_categories = category_client.get_all_categories()
      after_category_count = len(after_get_all_categories)

   with allure.step("Проверить, что категория не добавлена в базу данных"):
        db_category = spend_db.get_user_category_by_name(username, category_name)
        assert db_category is None

   with allure.step("Проверить тело ответа об ошибке"):
       assert excess_category.type == "niffler-spend: Bad request"
       assert excess_category.title == "Not Acceptable"
       assert excess_category.status == 406
       assert excess_category.detail == f"Can`t add over than 8 categories for user: '{username}'"
       assert excess_category.instance == "/api/categories/add"

   with allure.step("Проверить, что количество категорий не изменилось"):
       assert before_category_count == after_category_count


@allure.epic("Траты")
@allure.feature("Создание категории")
@allure.story("API")
@allure.tag("negative")
@allure.title("Пользователь не может создать дублирующую категорию")
@TestData.category("duplicate category")
def test_add_duplicate_category(
        category: CategoryModel,
        category_client: CategoryApiClient
):
   with allure.step("Получить количество категорий до добавления"):
      before_get_all_categories = category_client.get_all_categories()
      before_category_count = len(before_get_all_categories)

   with allure.step("Отправить запрос на добавление категории"):
      duplicate_category = category_client.add_category_error({"name": category.name})

   with allure.step("Получить количество категорий после добавления"):
      after_get_all_categories = category_client.get_all_categories()
      after_category_count = len(after_get_all_categories)

   with allure.step("Проверить тело ответа об ошибке"):
       assert duplicate_category.type == "niffler-spend: Bad request "
       assert duplicate_category.title == "Conflict"
       assert duplicate_category.status == 409
       assert duplicate_category.detail == "Cannot save duplicates"
       assert duplicate_category.instance == "/api/categories/add"

   with allure.step("Проверить, что количество категорий не изменилось"):
       assert before_category_count == after_category_count


@allure.epic("Траты")
@allure.feature("Создание категории")
@allure.story("API")
@allure.tag("negative")
@allure.title("Пользователь не может создать категорию с недопустимой длиной имени")
@pytest.mark.parametrize("category_name", ["1", "This text contains 51 simbols with chars and spaces"])
def test_add_category_invalid_name_length(
        user: tuple[str, str],
        category_name: str,
        category_client: CategoryApiClient,
        spend_db: SpendDB
):
   with allure.step("Получить количество категорий до добавления"):
      before_get_all_categories = category_client.get_all_categories()
      before_category_count = len(before_get_all_categories)

   with allure.step("Отправить запрос на добавление категории"):
       invalid_category = category_client.add_category_error({'name': category_name})

   with allure.step("Получить количество категорий после добавления"):
      after_get_all_categories = category_client.get_all_categories()
      after_category_count = len(after_get_all_categories)

   with allure.step("Проверить, что категория не добавлена в базу данных"):
        db_category = spend_db.get_user_category_by_name(user[0], category_name)
        assert db_category is None

   with allure.step("Проверить тело ответа об ошибке"):
       assert invalid_category.type == "niffler-gateway: Entity validation error"
       assert invalid_category.title == "Bad Request"
       assert invalid_category.status == 400
       assert invalid_category.detail == "Allowed category length should be from 2 to 50 characters"
       assert invalid_category.instance == "/api/categories/add"

   with allure.step("Проверить, что количество категорий не изменилось"):
       assert before_category_count == after_category_count


@allure.epic("Траты")
@allure.feature("Создание категории")
@allure.story("API")
@allure.tag("negative")
@allure.title("Пользователь не может создать категорию с пустым именем")
@pytest.mark.parametrize("category_name", [""])
def test_add_category_empty_str(
        user: tuple[str, str],
        category_name: str,
        category_client: CategoryApiClient,
        spend_db: SpendDB
):
   with allure.step("Получить количество категорий до добавления"):
      before_get_all_categories = category_client.get_all_categories()
      before_category_count = len(before_get_all_categories)

   with allure.step("Отправить запрос на добавление категории"):
       invalid_category = category_client.add_category_error({'name': category_name})

   with allure.step("Получить количество категорий после добавления"):
      after_get_all_categories = category_client.get_all_categories()
      after_category_count = len(after_get_all_categories)

   with allure.step("Проверить, что категория не добавлена в базу данных"):
        db_category = spend_db.get_user_category_by_name(user[0], category_name)
        assert db_category is None

   with allure.step("Проверить тело ответа об ошибке"):
       assert invalid_category.type == "niffler-gateway: Entity validation error"
       assert invalid_category.title == "Bad Request"
       assert invalid_category.status == 400
       assert "Category can not be blank" in invalid_category.detail
       assert "Allowed category length should be from 2 to 50 characters" in invalid_category.detail
       assert invalid_category.instance == "/api/categories/add"

   with allure.step("Проверить, что количество категорий не изменилось"):
       assert before_category_count == after_category_count
