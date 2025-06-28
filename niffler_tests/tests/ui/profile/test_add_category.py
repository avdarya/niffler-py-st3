from faker import Faker
from niffler_tests.clients.category_client import CategoryApiClient
from niffler_tests.web_pages.ProfilePage import ProfilePage

fake = Faker()

def test_add_category(
        profile_page: ProfilePage,
        go_to_profile_page: None,
        category_client: CategoryApiClient,
        update_category: dict
):
   category_name = fake.text(max_nb_chars=20).replace("\n", " ")

   profile_page.enter_add_category(category_name=category_name)
   profile_page.submit_add_category()

   alert_text = profile_page.alert_on_action()

   api_get_all_categories = category_client.get_all_categories()
   assert api_get_all_categories.status_code == 200
   body = api_get_all_categories.json()
   api_category_name = None
   api_category_id = None
   api_category_archived = None
   for category in body:
      if category["name"] == category_name:
         api_category_name = category["name"]
         api_category_id = category["id"]
         api_category_archived = category["archived"]

   update_category["name"] = category_name
   update_category["id"] = api_category_id
   update_category["archived"] = True

   assert category_name == api_category_name
   assert api_category_archived is False
   assert f"You've added new category: {category_name}" in alert_text
   assert profile_page.is_input_cleared()
   assert profile_page.invisible_category_chip(category_name=category_name) is False