import allure

from niffler_tests_python.clients.category_client import CategoryApiClient
from niffler_tests_python.databases.spend_db import SpendDB
from niffler_tests_python.utils.marks import TestData


@allure.epic('Spending management')
@allure.feature('[API-test] Category creation - Positive')
@allure.story('Get all categories')
@TestData.fill_categories
def test_get_all_categories_api(
        category_client: CategoryApiClient,
        spend_db: SpendDB
):
   with allure.step('Send request for fetch all categories'):
      all_categories = category_client.get_all_categories()
      api_names = {c.name for c in all_categories}
      api_ids = {c.id for c in all_categories}

   with allure.step('Fetch all categories in DB'):
        db_categories = spend_db.get_category_list()
        db_names = {c.name for c in db_categories}
        db_ids = {str(c.id) for c in db_categories}

   with allure.step('Assert get all categories'):
       with allure.step('Verify count of all categories from API'):
           assert len(all_categories) == len(db_categories)
       with allure.step('Verify category names from API'):
           assert set(api_names) == set(db_names)
       with allure.step('Verify category ids from API'):
           assert set(api_ids) == set(db_ids)
