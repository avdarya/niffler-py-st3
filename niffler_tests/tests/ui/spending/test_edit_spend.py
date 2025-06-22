import pytest
import os
from dateutil import tz
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

@pytest.mark.parametrize("amount, currency, spend_date, description", [
    ("456", "EUR", "02/09/2025", "spending for update")
])
def test_edit_spend(
        browser: WebDriver,
        config: ConfigProvider,
        add_spending: dict,
        update_category: dict,
        spend_client: SpendApiClient,
        amount: str,
        currency: str,
        spend_date: str,
        description: str,
):

    auth_browser = login(driver=browser, login_url=config.get_ui_auth_url(), username=user_login, password=password)

    main_page = MainPage(driver=auth_browser, config=config)
    spending_page = SpendingPage(driver=auth_browser)

    main_page.click_edit_spend(spend_id=add_spending["id"])

    spending_page.clear_amount_input()
    spending_page.enter_amount_input(amount=amount)

    spending_page.click_currency_input()
    spending_page.click_currency_value(currency_value=currency)

    new_category = fake.text(max_nb_chars=25).replace("\n", " ")
    spending_page.clear_category_input()
    spending_page.enter_category_input(category_name=new_category)

    spending_page.enter_date_input(spend_date=spend_date)

    spending_page.clear_description_input()
    spending_page.enter_description_input(description=description)

    spending_page.click_save_spend()

    alert_on_updated = main_page.alert_on_action()

    is_found_updated_row = main_page.is_found_spend_row(
        category_name=new_category,
        amount=amount,
        currency=currency,
        description=description,
        spend_date=spend_date,
    )

    api_spend = spend_client.get_all_spends()
    assert api_spend.status_code == 200
    for spend in api_spend.json():
        if spend["id"] == add_spending["id"]:
            local_dt = datetime.fromisoformat(spend["spendDate"]).astimezone(tz.tzlocal())
            date_str = local_dt.strftime("%m/%d/%Y")

            update_category["name"] = spend["category"]["name"]
            update_category["archived"] = True
            update_category["id"] = spend["category"]["id"]

            assert date_str == spend_date
            assert spend["category"]["name"] == new_category
            assert spend["currency"] == currency
            assert spend["amount"] == float(amount)
            assert spend["description"] == description

    assert "Spending is edited successfully" in alert_on_updated
    assert is_found_updated_row
