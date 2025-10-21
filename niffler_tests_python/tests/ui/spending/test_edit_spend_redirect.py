import allure
from datetime import datetime
from niffler_tests_python.clients.spend_client import SpendApiClient
from niffler_tests_python.model.spend import SpendModelAdd, SpendModel
from niffler_tests_python.utils.helpers import wait_for_spend_row
from niffler_tests_python.utils.marks import Pages, TestData
from niffler_tests_python.web_pages.MainPage import MainPage
from niffler_tests_python.web_pages.SpendingPage import SpendingPage


@allure.epic("Траты")
@allure.feature("Редактирование траты")
@allure.story("UI")
@allure.tag("positive")
@allure.title("Редирект на страницу редактирования траты")
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
    with allure.step('Сохраняем трату для редактирования'):
        spend_row = wait_for_spend_row(main_page, spend.id)
        assert spend_row is not None

    with allure.step('Открываем трату для редактирования'):
        main_page.click_edit_spend(spend_row)

    spending_page.expected_spend_url(spend.id)

    with allure.step('Получаем значения из полей формы редактирования'):
        amount_input = spending_page.get_amount_input()
        currency_input = spending_page.get_selected_currency_input()
        category_input = spending_page.get_category_input()
        description_input = spending_page.get_description_input()
        date_input = spending_page.get_date_input()
        date_input_formated = datetime.strptime(date_input, "%m/%d/%Y")
        spend_date_formated = spend.spendDate

    with allure.step('Проверяем корректность перехода на страницу редактирования'):
        with allure.step('Проверяем значение поля "Сумма"'):
            assert float(amount_input) == spend.amount
        with allure.step('Проверяем значение поля "Валюта"'):
            assert currency_input == spend.currency
        with allure.step('Проверяем значение поля "Категория"'):
            assert category_input == spend.category.name
        with allure.step('Проверяем значение поля "Дата"'):
            assert date_input_formated.date() == spend_date_formated.date()
        with allure.step('Проверяем значение поля "Описание"'):
            assert description_input == spend.description