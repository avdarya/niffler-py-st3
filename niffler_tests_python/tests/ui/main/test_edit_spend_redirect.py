import allure
from datetime import datetime
from niffler_tests_python.clients.spend_client import SpendApiClient
from niffler_tests_python.model.spend import SpendModelAdd, SpendModel
from niffler_tests_python.utils.marks import Pages, TestData
from niffler_tests_python.web_pages.MainPage import MainPage
from niffler_tests_python.web_pages.SpendingPage import SpendingPage


@allure.epic('Spending management')
@allure.feature('Spending update')
@allure.story('Redirect to edit spend')
@Pages.go_to_main_page_after_spend
@TestData.spend(SpendModelAdd(
    amount=203.01,
    description="test edit spend redirect",
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
    with allure.step('Save spend row for edit'):
        spend_row = main_page.get_spend_row(spend_id=spend.id)
        assert spend_row is not None

    with allure.step('Open spend for edit'):
        main_page.click_edit_spend(spend_row)

    with allure.step('Get values from edit form inputs'):
        amount_input = spending_page.get_amount_input()
        currency_input = spending_page.get_selected_currency_input()
        category_input = spending_page.get_category_input()
        description_input = spending_page.get_description_input()
        date_input = spending_page.get_date_input()
        date_input_formated = datetime.strptime(date_input, "%m/%d/%Y")
        spend_date_formated = spend.spendDate

    with allure.step('Assert edit spend redirect'):
        with allure.step('Verify amount field value'):
            assert float(amount_input) == spend.amount
        with allure.step('Verify currency field value'):
            assert currency_input == spend.currency
        with allure.step('Verify category field value'):
            assert category_input == spend.category.name
        with allure.step('Verify date field value'):
            assert date_input_formated.date() == spend_date_formated.date()
        with allure.step('Verify description field value'):
            assert description_input == spend.description