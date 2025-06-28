import pytest
import os
from dateutil import tz
import dotenv
from datetime import datetime
from faker import Faker
from niffler_tests.clients.spend_client import SpendApiClient
from niffler_tests.utils.api_checkers import assert_spend_record_exists
from niffler_tests.utils.helpers import wait_for_spend_row, is_text_match_spend_row
from niffler_tests.web_pages.HeaderPage import HeaderPage
from niffler_tests.web_pages.MainPage import MainPage
from niffler_tests.web_pages.SpendingPage import SpendingPage

fake = Faker()

@pytest.mark.parametrize("amount, currency, spend_date, description", [
    ("456", "EUR", "02/09/2025", "spending for update")
])
def test_edit_spend(
        main_page: MainPage,
        header_page: HeaderPage,
        spending_page: SpendingPage,
        add_spend: dict,
        update_category: dict,
        spend_client: SpendApiClient,
        amount: str,
        currency: str,
        spend_date: str,
        description: str,
):
    main_page.open()

    spend_row = main_page.get_spend_row(spend_id=add_spend["id"])
    main_page.click_edit_spend(spend_row)

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

    spend_row = wait_for_spend_row(main_page=main_page, spend_id=add_spend["id"])

    api_spending_resp = spend_client.get_all_spends()
    assert api_spending_resp.status_code == 200
    for spend in api_spending_resp.json():
        if spend["id"] == add_spend["id"]:
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
    assert is_text_match_spend_row(
        spend_row_text=spend_row.text,
        category_name=new_category,
        amount=amount,
        currency=currency,
        description=description,
        spend_date=spend_date
    )
