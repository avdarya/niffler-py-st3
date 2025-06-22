import pytest
import os
import dotenv
from faker import Faker
from selenium.webdriver.ie.webdriver import WebDriver
from clients.spend_client import SpendApiClient
from configuration.ConfigProvider import ConfigProvider
from utils.api_checkers import assert_spend_record_exists
from utils.helpers import login
from web_pages.HeaderPage import HeaderPage
from web_pages.MainPage import MainPage
from web_pages.SpendingPage import SpendingPage

dotenv.load_dotenv()
user_login = os.getenv("LOGIN")
password = os.getenv("PASSWORD")

fake = Faker()

@pytest.mark.parametrize("amount, currency, spend_date", [
    ("10.01", "RUB", "12/09/2024"),
    ("501", "KZT", "01/15/2025"),
    ("0.01", "EUR", "04/09/2025"),
    ("3", "USD", "06/21/2025")
])
def test_add_spending(
        browser: WebDriver,
        config: ConfigProvider,
        add_category: dict,
        spend_client: SpendApiClient,
        amount: str,
        currency: str,
        spend_date: str,
):

    auth_browser = login(driver=browser, login_url=config.get_ui_auth_url(), username=user_login, password=password)

    before_spending_resp = spend_client.get_all_spends()
    assert before_spending_resp.status_code == 200
    before_spending_count = len(before_spending_resp.json())

    header_page = HeaderPage(driver=auth_browser)
    main_page = MainPage(driver=auth_browser, config=config)
    spending_page = SpendingPage(driver=auth_browser)

    header_page.click_new_spending()

    spending_page.clear_amount_input()
    spending_page.enter_amount_input(amount)

    spending_page.click_currency_input()
    spending_page.click_currency_value(currency)

    category_name = add_category["name"]
    spending_page.click_category(category_name=category_name)

    spending_page.enter_date_input(spend_date=spend_date)

    description = fake.sentence(nb_words=5)
    spending_page.enter_description_input(description=description)

    spending_page.click_save_spend()

    alert_on_added = main_page.alert_on_action()
    assert "New spending is successfully created" in alert_on_added

    is_spend_in_table = main_page.is_found_spend_row(
        category_name=add_category["name"],
        amount=amount,
        currency=currency,
        description=description,
        spend_date=spend_date
    )

    assert is_spend_in_table

    after_spending_resp = spend_client.get_all_spends()
    assert after_spending_resp.status_code == 200
    after_spending_count = len(after_spending_resp.json())
    assert before_spending_count == after_spending_count - 1

    spend_id = assert_spend_record_exists(
        api_response=after_spending_resp.json(),
        currency=currency,
        amount=amount,
        spend_date=spend_date,
        description=description,
        category_name=add_category["name"],
        spend_client=spend_client,
    )["id"]
    spend_client.delete_spending([spend_id])