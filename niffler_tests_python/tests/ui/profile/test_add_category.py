import pytest

from niffler_tests_python.clients.category_client import CategoryApiClient
from niffler_tests_python.databases.spend_db import SpendDB
from niffler_tests_python.tests.conftest import Pages, TestData
from niffler_tests_python.web_pages.ProfilePage import ProfilePage


@Pages.go_to_profile_page
@pytest.mark.parametrize("category_name", ["added category"])
def test_add_category(
        profile_page: ProfilePage,
        category_client: CategoryApiClient,
        spend_db: SpendDB,
        category_name: str
):
   profile_page.enter_add_category(category_name=category_name)
   profile_page.submit_add_category()
   alert_text = profile_page.alert_on_action()

   api_get_all_categories = category_client.get_all_categories()
   # api_category_id = None
   api_category_archived = None
   for category_item in api_get_all_categories:
      if category_item.name == category_name:
         # api_category_id = category_item.id
         api_category_archived = category_item.archived

   db_category = spend_db.get_category_by_name(name=category_name)
   spend_db.delete_category(db_category.id)

   assert api_category_archived is False
   assert f"You've added new category: {category_name}" in alert_text
   assert profile_page.is_input_cleared()
   assert profile_page.invisible_category_chip(category_name=category_name) is False
   assert db_category.name == category_name
   assert db_category.archived is False