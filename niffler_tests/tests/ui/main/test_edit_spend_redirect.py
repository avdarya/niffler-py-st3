import os
import dotenv
from datetime import datetime
from faker import Faker
from selenium.webdriver.ie.webdriver import WebDriver
from clients.spend_client import SpendApiClient
from configuration.ConfigProvider import ConfigProvider
from tests.conftest import update_category
from utils.helpers import login
from web_pages.MainPage import MainPage
from web_pages.SpendingPage import SpendingPage

dotenv.load_dotenv()
user_login = os.getenv("LOGIN")
password = os.getenv("PASSWORD")

fake = Faker()

def test_edit_spend_redirect(
        browser: WebDriver,
        config: ConfigProvider,
        add_spending: dict,
        update_category: dict,
        spend_client: SpendApiClient
):

    auth_browser = login(driver=browser, login_url=config.get_ui_auth_url(), username=user_login, password=password)

    main_page = MainPage(driver=auth_browser, config=config)
    spending_page = SpendingPage(driver=auth_browser)

    main_page.click_edit_spend(spend_id=add_spending["id"])

    amount_input = spending_page.get_amount_input()
    currency_input = spending_page.get_selected_currency_input()
    category_input = spending_page.get_category_input()
    description_input = spending_page.get_description_input()

    date_input = spending_page.get_date_input()
    date_input_formated = datetime.strptime(date_input, "%m/%d/%Y")
    spend_date_formated = datetime.fromisoformat(add_spending["spendDate"])

    assert float(amount_input) == add_spending["amount"]
    assert currency_input == add_spending["currency"]
    assert category_input == add_spending["category"]["name"]
    assert date_input_formated.date() == spend_date_formated.date()
    assert description_input == add_spending["description"]