import dotenv
import os
from faker import Faker
from selenium.webdriver.ie.webdriver import WebDriver
from clients.categories_client import CategoriesApiClient
from configuration.ConfigProvider import ConfigProvider
from utils.helpers import login
from web_pages.HeaderPage import HeaderPage
from web_pages.ProfilePage import ProfilePage

dotenv.load_dotenv()
user_login = os.getenv("LOGIN")
password = os.getenv("PASSWORD")

fake = Faker()

def test_add_empty_category(
        browser: WebDriver,
        config: ConfigProvider,
        categories_client: CategoriesApiClient,
):
   auth_browser = login(driver=browser, login_url=config.get_ui_auth_url(), username=user_login, password=password)

   header_page = HeaderPage(driver=auth_browser)
   header_page.click_menu_button()
   header_page.click_profile()

   profile_page = ProfilePage(driver=auth_browser)

   before_get_all_categories = categories_client.get_all_categories()
   assert before_get_all_categories.status_code == 200
   before_category_count = len(before_get_all_categories.json())

   profile_page.submit_add_empty_category()

   after_get_all_categories = categories_client.get_all_categories()
   assert after_get_all_categories.status_code == 200
   after_category_count = len(after_get_all_categories.json())

   assert before_category_count == after_category_count
   assert "Allowed category length is from 2 to 50 symbols" in profile_page.helper_text_empty_add_category()
