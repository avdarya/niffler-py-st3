from faker import Faker
from niffler_tests.clients.category_client import CategoryApiClient
from niffler_tests.utils.helpers import wait_for_category_update_name
from niffler_tests.web_pages.HeaderPage import HeaderPage
from niffler_tests.web_pages.MainPage import MainPage
from niffler_tests.web_pages.ProfilePage import ProfilePage

fake = Faker()


def test_edit_category_by_icon(
        profile_page: ProfilePage,
        add_category: dict,
        go_to_profile_page: None,
        category_client: CategoryApiClient,
):
   category_name = add_category["name"]
   category_id = add_category["id"]
   new_category_name = fake.text(max_nb_chars=10).replace("\n", " ")

   profile_page.click_edit_category_icon(category_name=category_name)
   expected_text_input = profile_page.text_edit_category_input()

   profile_page.clear_edit_category_input()
   profile_page.enter_edit_category(category_name=new_category_name)
   profile_page.submit_edit_category()

   alert_text = profile_page.alert_on_action()

   updated_category = wait_for_category_update_name(
      categories_client=category_client,
      category_id=category_id,
      expected_name=new_category_name
   )

   api_get_all_categories = category_client.get_all_categories()
   assert api_get_all_categories.status_code == 200
   body = api_get_all_categories.json()
   for category in body:
      if category["id"] == category_id:
         assert category["name"] == new_category_name
         assert category["archived"] is False

   assert expected_text_input == category_name
   assert "Category name is changed" in alert_text
   assert profile_page.invisible_category_chip(category_name=new_category_name) is False
   assert updated_category["archived"] is False

def test_cancel_edit_category(
        profile_page: ProfilePage,
        add_category: dict,
        go_to_profile_page: None,
        category_client: CategoryApiClient,
):
   category_name = add_category["name"]
   category_id = add_category["id"]

   profile_page.click_category_chip(category_name=category_name)
   profile_page.click_close_edit_category()

   is_category_chip_present = profile_page.invisible_category_chip(category_name=category_name)

   api_category = wait_for_category_update_name(
      categories_client=category_client,
      category_id=category_id,
      expected_name=category_name
   )

   assert is_category_chip_present is False
   assert api_category["archived"] is False
