from niffler_tests_python.clients.category_client import CategoryApiClient
from niffler_tests_python.databases.spend_db import SpendDB
from niffler_tests_python.model.category import CategoryModel
from niffler_tests_python.tests.conftest import Pages, TestData
from niffler_tests_python.utils.helpers import wait_for_category_update_archive
from niffler_tests_python.web_pages.ProfilePage import ProfilePage


@Pages.go_to_profile_after_category
@TestData.category("category for archive")
def test_archive_category(
        category: CategoryModel,
        profile_page: ProfilePage,
        category_client: CategoryApiClient,
        spend_db: SpendDB
):
   category_name = category.name
   category_id = category.id

   profile_page.click_archive_category_icon(category_name=category_name)
   alert_dialog_title = profile_page.alert_dialog_title()
   alert_dialog_description = profile_page.alert_dialog_description()
   profile_page.click_archive_category_button()
   alert_text = profile_page.alert_on_action()

   wait_for_category_update_archive(
      categories_client=category_client,
      category_id=category_id,
      expected_archive=True
   )

   db_category = spend_db.get_category_by_name(category_name)

   assert alert_dialog_title == "Archive category"
   assert category_name in alert_dialog_description
   assert category_name in alert_text
   assert profile_page.invisible_category_chip(category_name=category_name) is True
   assert db_category.archived is True

@TestData.archive_category("category for unarchive")
def test_unarchive_category(
        profile_page: ProfilePage,
        archive_category: CategoryModel,
        go_to_profile_page: None,
        category_client: CategoryApiClient,
        spend_db: SpendDB
):
   category_name = archive_category.name
   category_id = archive_category.id

   profile_page.click_show_archived()
   profile_page.click_unarchive_category_icon(category_name=category_name)
   alert_dialog_title = profile_page.alert_dialog_title()
   alert_dialog_description = profile_page.alert_dialog_description()
   profile_page.click_unarchive_category_button()
   text_alert_archive = profile_page.alert_on_action()

   is_active_category_chip = profile_page.is_active_category_chip(category_name=category_name)
   is_display_edit_icon = profile_page.is_display_edit_icon(category_name=category_name)
   is_display_archive_icon = profile_page.is_display_archive_icon(category_name=category_name)

   wait_for_category_update_archive(
      categories_client=category_client,
      category_id=category_id,
      expected_archive=False
   )

   db_category = spend_db.get_category_by_name(category_name)

   assert alert_dialog_title == "Unarchive category"
   assert category_name in alert_dialog_description
   assert category_name in text_alert_archive
   assert is_active_category_chip == True
   assert is_display_edit_icon == True
   assert is_display_archive_icon == True
   assert db_category.archived is False
