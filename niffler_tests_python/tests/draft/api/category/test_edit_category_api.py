import allure
import pytest

from niffler_tests_python.clients.category_client import CategoryApiClient
from niffler_tests_python.databases.spend_db import SpendDB
from niffler_tests_python.model.category import CategoryModel
from niffler_tests_python.utils.marks import TestData
from niffler_tests_python.utils.helpers import get_category_by_name


@allure.epic('Spending management')
@allure.feature('[API-test] Category updating - Positive')
@allure.story('Edit category')
@TestData.category("category for edit")
@pytest.mark.parametrize("new_category_name", ["updated category"])
def test_edit_category_by_icon(
        category: CategoryModel,
        category_client: CategoryApiClient,
        spend_db: SpendDB,
        new_category_name: str,
        username: str
):
    with allure.step('Send request for edit category'):
        data_for_edit = CategoryModel(
            id=category.id,
            name=new_category_name,
            username=username,
            archived=not category.archived
        )
        edited_category = category_client.update_category(data_for_edit)

    with allure.step('Retrieve all categories from API and search edited category'):
        api_category = get_category_by_name(new_category_name, category_client)

    with allure.step('Retrieve added category in DB'):
        db_category = spend_db.get_category_by_id(category.id)

    with allure.step('Assert only name, archived changed for edited category'):
        with allure.step('Verify response data for edited category'):
            assert edited_category.name == new_category_name
            assert edited_category.archived != category.archived
            assert edited_category.username == username
        with allure.step('Verify added category data in API'):
            assert api_category.name == new_category_name
            assert api_category.archived != category.archived
            assert api_category.username == username
        with allure.step('Verify added category data in DB'):
            assert db_category.name == new_category_name
            assert db_category.archived != category.archived
            assert db_category.username == username