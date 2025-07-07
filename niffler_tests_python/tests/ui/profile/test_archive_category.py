import allure

from niffler_tests_python.clients.category_client import CategoryApiClient
from niffler_tests_python.databases.spend_db import SpendDB
from niffler_tests_python.model.category import CategoryModel
from niffler_tests_python.tests.conftest import Pages, TestData
from niffler_tests_python.utils.helpers import wait_for_category_update_archive
from niffler_tests_python.web_pages.ProfilePage import ProfilePage


@allure.epic('Spending management')
@allure.feature('Category archiving')
@allure.story('Archive category')
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

   with allure.step('Click archive icon'):
      profile_page.click_archive_category_icon(category_name=category_name)

   with allure.step('Save submit dialog text'):
      dialog_title = profile_page.submit_dialog_title()
      dialog_description = profile_page.submit_dialog_description()

   with allure.step('Submit archived category'):
      profile_page.click_archive_category_button()

   with allure.step('Save alert dialog'):
      alert_text = profile_page.alert_on_action()

   with allure.step('Retrieve archived category from API'):
      wait_for_category_update_archive(
         categories_client=category_client,
         category_id=category_id,
         expected_archive=True
      )

   with allure.step('Retrieve archived category in DB'):
      db_category = spend_db.get_category_by_name(category_name)

   with allure.step('Assert archived category'):
      with allure.step('Verify submit dialog title and description'):
         assert dialog_title == "Archive category"
         assert category_name in dialog_description
      with allure.step('Verify category name in alert text'):
         assert category_name in alert_text
      with allure.step('Verify category chip is invisible in UI'):
         assert profile_page.invisible_category_chip(category_name=category_name) is True
      with allure.step('Verify category in DB is archived'):
         assert db_category.archived is True

@allure.epic('Spending management')
@allure.feature('Category archiving')
@allure.story('Unarchive category')
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

   with allure.step('Click show archived toggle button'):
      profile_page.click_show_archived()

   with allure.step('Click unarchive icon'):
      profile_page.click_unarchive_category_icon(category_name=category_name)

   with allure.step('Save submit dialog text'):
      dialog_title = profile_page.submit_dialog_title()
      dialog_description = profile_page.submit_dialog_description()

   with allure.step('Submit unarchived category'):
      profile_page.click_unarchive_category_button()

   with allure.step('Save alert dialog'):
      alert_text = profile_page.alert_on_action()

   with allure.step('Update unarchived category from UI'):
      is_active_category_chip = profile_page.is_active_category_chip(category_name=category_name)
      is_display_edit_icon = profile_page.is_display_edit_icon(category_name=category_name)
      is_display_archive_icon = profile_page.is_display_archive_icon(category_name=category_name)

   with allure.step('Retrieve unarchived category from API'):
      wait_for_category_update_archive(
         categories_client=category_client,
         category_id=category_id,
         expected_archive=False
      )

   with allure.step('Retrieve unarchived category in DB'):
      db_category = spend_db.get_category_by_name(category_name)

   with allure.step('Assert archived category'):
      with allure.step('Verify submit dialog title and description'):
         assert dialog_title == "Unarchive category"
         assert category_name in dialog_description
      with allure.step('Verify category name in alert text'):
         assert category_name in alert_text
      with allure.step('Verify category chip is active in UI'):
         assert is_active_category_chip == True
      with allure.step('Verify category row contains edit icon in UI'):
         assert is_display_edit_icon == True
      with allure.step('Verify category row contains archive icon in UI'):
         assert is_display_archive_icon == True
   with allure.step('Verify category in DB is unarchived'):
      assert db_category.archived is False
