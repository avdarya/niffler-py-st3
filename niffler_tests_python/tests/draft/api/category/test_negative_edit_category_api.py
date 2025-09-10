import allure
import pytest

from niffler_tests_python.clients.category_client import CategoryApiClient
from niffler_tests_python.databases.spend_db import SpendDB
from niffler_tests_python.model.category import CategoryModel
from niffler_tests_python.utils.helpers import get_category_by_name


@allure.epic('Spending management')
@allure.feature('[API-test] Category creation - Negative')
@allure.story('Attempt change category name on existing category')
@pytest.mark.parametrize("two_categories", [("category 1", "category 2")], indirect=True)
def test_change_category_name_for_existing_category(
        two_categories: tuple[CategoryModel, CategoryModel],
        category_client: CategoryApiClient,
        spend_db: SpendDB
):
    category_1, category_2 = two_categories

    with allure.step('Send request to change name for first category to an existing one'):
      edited_category_1 = category_client.update_category_error(
          {
              "id": category_1.id,
              "name": category_2.name,
          }
      )

    with allure.step('Retrieve all categories from API and search category_1'):
        api_category_1 = get_category_by_name(category_1.name, category_client)

    with allure.step('Retrieve category_1 in DB'):
       db_category_1 = spend_db.get_category_by_id(category_1.id)

    with allure.step('Assert category name does not change to an existing one'):
       with allure.step('Verify response for change name to existing one'):
           assert edited_category_1.type == "niffler-spend: Bad request "
           assert edited_category_1.title ==  "Conflict"
           assert edited_category_1.status == 409
           assert edited_category_1.detail == "Cannot save duplicates"
           assert edited_category_1.instance == "/api/categories/update"
       with allure.step('Verify category_1 does not change in API'):
           assert api_category_1.name == category_1.name
       with allure.step('Verify category_1 does not change in DB'):
           assert db_category_1.name == category_1.name