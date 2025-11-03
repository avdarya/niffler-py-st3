import allure

from niffler_tests_python.clients.category_client import CategoryApiClient
from niffler_tests_python.databases.spend_db import SpendDB
from niffler_tests_python.utils.marks import TestData


@allure.epic("Траты")
@allure.feature("Получение категорий")
@allure.story("API")
@allure.tag("positive")
@allure.title("Пользователь может получить список всех категорий")
@TestData.fill_categories
def test_get_all_categories_api(
        category_client: CategoryApiClient,
        user: tuple[str, str],
        spend_db: SpendDB
):
   with allure.step('Отправить запрос на получение всех категорий через API.'):
       all_categories = category_client.get_all_categories()
       api_names = {c.name for c in all_categories}
       api_ids = {c.id for c in all_categories}

   with allure.step('Получить список всех категорий из базы данных.'):
       db_categories = spend_db.get_user_categories(user[0])
       db_names = {c.name for c in db_categories}
       db_ids = {str(c.id) for c in db_categories}

   with allure.step('Проверить, что количество категорий в API и БД совпадает'):
       assert len(all_categories) == len(db_categories), (
           f"Ожидалось {len(db_categories)} категорий из БД, но в API получено {len(all_categories)}"
       )
   with allure.step('Проверить, что названия категорий в API и БД совпадают'):
       assert set(api_names) == set(db_names), (
           f"Названия категорий в API {api_names} не совпадают с БД {db_names}"
       )
   with allure.step('Проверить, что ID категорий в API и БД совпадают'):
       assert set(api_ids) == set(db_ids), (
           f"ID категорий в API {api_ids} не совпадают с БД {db_ids}"
       )
