from datetime import datetime
from niffler_tests_python.clients.spend_client import SpendApiClient
from niffler_tests_python.model.spend import SpendModelAdd, SpendModel
from niffler_tests_python.tests.conftest import Pages, TestData
from niffler_tests_python.web_pages.MainPage import MainPage
from niffler_tests_python.web_pages.SpendingPage import SpendingPage


@Pages.go_to_main_page_after_spend
@TestData.spend(SpendModelAdd(
    amount=203.01,
    description="test_edit_spend_redirect",
    currency="USD",
    spendDate="2025-06-26",
    category={"name": "edit spend"}
))
def test_edit_spend_redirect(
        main_page: MainPage,
        spending_page: SpendingPage,
        spend: SpendModel,
        spend_client: SpendApiClient,
):
    spend_row = main_page.get_spend_row(spend_id=spend.id)
    assert spend_row is not None

    main_page.click_edit_spend(spend_row)

    amount_input = spending_page.get_amount_input()
    currency_input = spending_page.get_selected_currency_input()
    category_input = spending_page.get_category_input()
    description_input = spending_page.get_description_input()

    date_input = spending_page.get_date_input()
    date_input_formated = datetime.strptime(date_input, "%m/%d/%Y")
    spend_date_formated = spend.spendDate

    assert float(amount_input) == spend.amount
    assert currency_input == spend.currency
    assert category_input == spend.category.name
    assert date_input_formated.date() == spend_date_formated.date()
    assert description_input == spend.description