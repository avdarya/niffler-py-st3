import allure
import pytest

from niffler_tests_python.clients.category_client import CategoryApiClient
from niffler_tests_python.databases.spend_db import SpendDB
from niffler_tests_python.model.category import CategoryModel
from niffler_tests_python.utils.marks import TestData


@allure.epic('Spending management')
@allure.feature('[API-test] Category creation - Negative')
@allure.story('Attempt add over than 8 categories for user')
@TestData.fill_categories
@pytest.mark.parametrize("category_name", ["excess category"])
def test_add_over_category(
        category_name: str,
        category_client: CategoryApiClient,
        username: str,
        spend_db: SpendDB
):
   with allure.step('Retrieve category count before'):
      before_get_all_categories = category_client.get_all_categories()
      before_category_count = len(before_get_all_categories)

   with allure.step('Send request for added excess category'):
      excess_category = category_client.add_category_error({"name": category_name})

   with allure.step('Retrieve category count after'):
      after_get_all_categories = category_client.get_all_categories()
      after_category_count = len(after_get_all_categories)

   with allure.step('Search category in DB by name'):
        db_category = spend_db.get_category_by_name(category_name)

   with allure.step('Assert excess category does not add'):
       with allure.step('Verify response for added duplicate category'):
           assert excess_category.type == "niffler-spend: Bad request"
           assert excess_category.title ==  "Not Acceptable"
           assert excess_category.status == 406
           assert excess_category.detail == f"Can`t add over than 8 categories for user: '{username}'"
           assert excess_category.instance == "/api/categories/add"
       with allure.step('Category count after = category count before'):
           assert before_category_count == after_category_count
       with allure.step('Verify excess category absent in DB'):
           assert db_category is None

@allure.epic('Spending management')
@allure.feature('[API-test] Category creation - Negative')
@allure.story('Attempt add duplicate category')
@TestData.category("duplicate category")
def test_add_duplicate_category(
        category: CategoryModel,
        category_client: CategoryApiClient
):
   with allure.step('Retrieve category count before'):
      before_get_all_categories = category_client.get_all_categories()
      before_category_count = len(before_get_all_categories)

   with allure.step('Send request for added duplicate category'):
      duplicate_category = category_client.add_category_error({"name": category.name})

   with allure.step('Retrieve category count after'):
      after_get_all_categories = category_client.get_all_categories()
      after_category_count = len(after_get_all_categories)

   with allure.step('Assert add duplicate category'):
       with allure.step('Verify response for added duplicate category'):
           assert duplicate_category.type == "niffler-spend: Bad request "
           assert duplicate_category.title ==  "Conflict"
           assert duplicate_category.status == 409
           assert duplicate_category.detail == "Cannot save duplicates"
           assert duplicate_category.instance == "/api/categories/add"
       with allure.step('Category count after = category count before'):
           assert before_category_count == after_category_count

@allure.epic('Spending management')
@allure.feature('[API-test] Category creation - Negative')
@allure.story('Attempt add category with invalid length of name')
@pytest.mark.parametrize("category_name", ["1", "This text contains 51 simbols with chars and spaces"])
def test_add_category_invalid_name_length(
        category_name: str,
        category_client: CategoryApiClient,
        spend_db: SpendDB
):
   with allure.step('Retrieve category count before'):
      before_get_all_categories = category_client.get_all_categories()
      before_category_count = len(before_get_all_categories)

   with allure.step(f'Send request for edit category with length of name = {len(category_name)}'):
       invalid_category = category_client.add_category_error({'name': category_name})

   with allure.step('Retrieve category count after'):
      after_get_all_categories = category_client.get_all_categories()
      after_category_count = len(after_get_all_categories)

   with allure.step('Search category in DB by name'):
        db_category = spend_db.get_category_by_name(category_name)

   with allure.step('Assert add category with invalid value'):
       with allure.step('Verify response for added invalid category'):
           assert invalid_category.type == "niffler-gateway: Entity validation error"
           assert invalid_category.title ==  "Bad Request"
           assert invalid_category.status == 400
           assert invalid_category.detail == "Allowed category length should be from 2 to 50 characters"
           assert invalid_category.instance == "/api/categories/add"
       with allure.step('Category count after = category count before'):
           assert before_category_count == after_category_count
       with allure.step('Verify invalid category absent in DB'):
           assert db_category is None

@allure.epic('Spending management')
@allure.feature('[API-test] Category creation - Negative')
@allure.story('Attempt add category with empty string')
@pytest.mark.parametrize("category_name", [""])
def test_add_category_empty_str(
        category_name: str,
        category_client: CategoryApiClient,
        spend_db: SpendDB
):
   with allure.step('Retrieve category count before'):
      before_get_all_categories = category_client.get_all_categories()
      before_category_count = len(before_get_all_categories)

   with allure.step(f'Send request for edit category with length of name = {len(category_name)}'):
       invalid_category = category_client.add_category_error({'name': category_name})

   with allure.step('Retrieve category count after'):
      after_get_all_categories = category_client.get_all_categories()
      after_category_count = len(after_get_all_categories)

   with allure.step('Search category in DB by name'):
        db_category = spend_db.get_category_by_name(category_name)

   with (allure.step('Assert add category with invalid value')):
       with allure.step('Verify response for added invalid category'):
           assert invalid_category.type == "niffler-gateway: Entity validation error"
           assert invalid_category.title ==  "Bad Request"
           assert invalid_category.status == 400
           assert "Category can not be blank" in invalid_category.detail
           assert "Allowed category length should be from 2 to 50 characters" in invalid_category.detail
           assert invalid_category.instance == "/api/categories/add"
       with allure.step('Category count after = category count before'):
           assert before_category_count == after_category_count
       with allure.step('Verify invalid category absent in DB'):
           assert db_category is None
