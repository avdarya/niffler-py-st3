import allure
import pytest

from niffler_tests_python.clients.category_client import CategoryApiClient
from niffler_tests_python.databases.spend_db import SpendDB
from niffler_tests_python.utils.helpers import get_category_by_name


@allure.epic('Spending management')
@allure.feature('[API-test] Category creation - Positive')
@allure.story('Add category')
@pytest.mark.parametrize("category_name", ["added category"])
def test_add_category_and_verify_data(
        category_client: CategoryApiClient,
        spend_db: SpendDB,
        category_name: str,
        username: str
):
    with allure.step('Retrieve category count before'):
        before_get_all_categories = category_client.get_all_categories()
        before_category_count = len(before_get_all_categories)

    with allure.step('Send request for add category'):
        added_category = category_client.add_category(category_name=category_name)

    with allure.step('Retrieve all categories from API and search added category'):
        api_category = get_category_by_name(category_name, category_client)

    with allure.step('Retrieve category count after'):
        after_get_all_categories = category_client.get_all_categories()
        after_category_count = len(after_get_all_categories)

    with allure.step('Retrieve added category in DB'):
       db_category = spend_db.get_category_by_id(added_category.id)
       with allure.step('Delete added category'):
          spend_db.delete_category(db_category.id)

    with allure.step('Assert added category name, archived, username'):
        with allure.step('Verify response data for added category'):
            assert added_category.name == category_name
            assert added_category.archived is False
            assert added_category.username == username
        with allure.step('Category count before = category count after - 1'):
            assert before_category_count == after_category_count - 1
        with allure.step('Verify added category data in API'):
            assert api_category.name == category_name
            assert api_category.archived is False
            assert api_category.username == username
        with allure.step('Verify added category data in DB'):
            assert db_category.name == category_name
            assert db_category.archived is False
            assert db_category.username == username
