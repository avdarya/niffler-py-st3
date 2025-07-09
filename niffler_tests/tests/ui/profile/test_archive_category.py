from niffler_tests.clients.category_client import CategoryApiClient
from niffler_tests.utils.helpers import wait_for_category_update_archive
from niffler_tests.web_pages.ProfilePage import ProfilePage

def test_archive_category(
        add_category: dict,
        profile_page: ProfilePage,
        go_to_profile_page: None,
        category_client: CategoryApiClient,
):
   category_name = add_category["name"]
   category_id = add_category["id"]

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

   assert alert_dialog_title == "Archive category"
   assert category_name in alert_dialog_description
   assert category_name in alert_text
   assert profile_page.invisible_category_chip(category_name=category_name) is True

def test_unarchive_category(
        profile_page: ProfilePage,
        add_archive_category: dict,
        go_to_profile_page: None,
        category_client: CategoryApiClient,
):
   category_name = add_archive_category["name"]
   category_id = add_archive_category["id"]

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

   assert alert_dialog_title == "Unarchive category"
   assert category_name in alert_dialog_description
   assert category_name in text_alert_archive
   assert is_active_category_chip == True
   assert is_display_edit_icon == True
   assert is_display_archive_icon == True
