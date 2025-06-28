import pytest
from faker import Faker

from niffler_tests.clients.spend_client import SpendApiClient
from niffler_tests.utils.api_checkers import assert_spend_record_exists
from niffler_tests.utils.helpers import wait_for_spend_row, is_text_match_spend_row
from niffler_tests.web_pages.HeaderPage import HeaderPage
from niffler_tests.web_pages.MainPage import MainPage
from niffler_tests.web_pages.SpendingPage import SpendingPage

fake = Faker()

@pytest.mark.parametrize("amount, currency, spend_date", [
    ("10.01", "RUB", "12/09/2024"),
    ("501", "KZT", "01/15/2025"),
    ("0.01", "EUR", "04/09/2025"),
    ("3", "USD", "06/21/2025")
])
def test_add_spending(
        main_page: MainPage,
        header_page: HeaderPage,
        spending_page: SpendingPage,
        add_category: dict,
        spend_client: SpendApiClient,
        amount: str,
        currency: str,
        spend_date: str,
):
    main_page.open()

    before_spending_resp = spend_client.get_all_spends()
    assert before_spending_resp.status_code == 200
    before_spending_count = len(before_spending_resp.json())

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

    spend_row = wait_for_spend_row(main_page=main_page, spend_id=spend_id)

    spend_client.delete_spending([spend_id])

    assert "New spending is successfully created" in alert_on_added
    assert spend_row is not None
    assert is_text_match_spend_row(
        spend_row_text=spend_row.text,
        category_name=add_category["name"],
        amount=amount,
        currency=currency,
        description=description,
        spend_date=spend_date
    )
