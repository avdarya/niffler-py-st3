import pytest
from datetime import datetime
from dateutil.tz import tz
from niffler_tests_python.clients.spend_client import SpendApiClient
from niffler_tests_python.databases.spend_db import SpendDB
from niffler_tests_python.model.spend import SpendModelAdd, SpendModel
from niffler_tests_python.tests.conftest import Pages, TestData
from niffler_tests_python.utils.helpers import wait_for_spend_row, is_text_match_spend_row
from niffler_tests_python.web_pages.MainPage import MainPage
from niffler_tests_python.web_pages.SpendingPage import SpendingPage


@Pages.go_to_main_page_after_spend
@TestData.spend(SpendModelAdd(
    amount=203.01,
    description="test_edit_spend",
    currency="USD",
    spendDate="2025-06-26T21:00:00.000+00:00",
    category={"name": "edit spend"}
))
@pytest.mark.parametrize("amount, currency, new_category, spend_date, description", [
    ("456", "EUR", "after edit spend", "02/09/2025", "spending for update")
])
def test_edit_spend(
        main_page: MainPage,
        spending_page: SpendingPage,
        spend: SpendModel,
        spend_client: SpendApiClient,
        spend_db: SpendDB,
        amount: str,
        currency: str,
        new_category: str,
        spend_date: str,
        description: str,
):
    added_spend_row = main_page.get_spend_row(spend_id=spend.id)
    main_page.click_edit_spend(added_spend_row)

    spending_page.clear_amount_input()
    spending_page.enter_amount_input(amount=amount)

    spending_page.click_currency_input()
    spending_page.click_currency_value(currency_value=currency)

    spending_page.clear_category_input()
    spending_page.enter_category_input(category_name=new_category)

    spending_page.enter_date_input(spend_date=spend_date)

    spending_page.clear_description_input()
    spending_page.enter_description_input(description=description)

    spending_page.click_save_spend()

    alert_on_updated = main_page.alert_on_action()

    updated_spend_row = wait_for_spend_row(main_page=main_page, spend_id=spend.id)

    api_spend = spend_client.get_all_spends()
    for api_spend in api_spend:
        if api_spend.id == spend.id:
            local_dt = api_spend.spendDate.astimezone(tz.tzlocal())
            date_str = local_dt.strftime("%m/%d/%Y")
            assert date_str == spend_date
            assert api_spend.category.name == new_category
            assert api_spend.currency == currency
            assert api_spend.amount == float(amount)
            assert api_spend.description == description

    db_spend = spend_db.get_spend(spend_id=spend.id)
    db_category = spend_db.get_category_by_name(name=new_category)

    assert "Spending is edited successfully" in alert_on_updated
    assert is_text_match_spend_row(
        spend_row_text=updated_spend_row.text,
        category_name=new_category,
        amount=amount,
        currency=currency,
        description=description,
        spend_date=spend_date
    )
    assert db_spend.amount == float(amount)
    assert db_spend.currency == currency
    assert db_spend.spend_date == datetime.strptime(spend_date, "%m/%d/%Y").date()
    assert db_spend.description == description
    assert db_category.name == new_category
