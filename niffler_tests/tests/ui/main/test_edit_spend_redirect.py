from datetime import datetime
from niffler_tests.clients.spend_client import SpendApiClient
from niffler_tests.web_pages.MainPage import MainPage
from niffler_tests.web_pages.SpendingPage import SpendingPage


def test_edit_spend_redirect(
        main_page: MainPage,
        spending_page: SpendingPage,
        add_spend: dict,
        update_category: dict,
        spend_client: SpendApiClient
):
    main_page.open()

    spend_row = main_page.get_spend_row(spend_id=add_spend["id"])
    assert spend_row is not None

    main_page.click_edit_spend(spend_row)

    amount_input = spending_page.get_amount_input()
    currency_input = spending_page.get_selected_currency_input()
    category_input = spending_page.get_category_input()
    description_input = spending_page.get_description_input()

    date_input = spending_page.get_date_input()
    date_input_formated = datetime.strptime(date_input, "%m/%d/%Y")
    spend_date_formated = datetime.fromisoformat(add_spend["spendDate"])

    assert float(amount_input) == add_spend["amount"]
    assert currency_input == add_spend["currency"]
    assert category_input == add_spend["category"]["name"]
    assert date_input_formated.date() == spend_date_formated.date()
    assert description_input == add_spend["description"]