import allure
import pytest
from datetime import datetime
from dateutil.tz import tz
from niffler_tests_python.clients.spend_client import SpendApiClient
from niffler_tests_python.databases.spend_db import SpendDB
from niffler_tests_python.model.enums.currency_title import CurrencyTitle
from niffler_tests_python.model.rest_model.spend import SpendModelAdd, SpendModel
from niffler_tests_python.utils.marks import Pages, TestData
from niffler_tests_python.utils.helpers import wait_for_spend_row, is_text_match_spend_row
from niffler_tests_python.web_pages.MainPage import MainPage
from niffler_tests_python.web_pages.SpendingPage import SpendingPage


@allure.epic("Траты")
@allure.feature("Редактирование траты")
@allure.story("UI")
@allure.tag("positive")
@allure.title("Редактирование траты — обновление записи в БД и на странице /main")
@Pages.go_to_main_page_after_spend
@TestData.spend(SpendModelAdd(
    amount=203.01,
    description="test edit spend",
    currency=CurrencyTitle.USD.value,
    spendDate="2025-06-26",
    category={"name": "edit spend"}
))
@pytest.mark.parametrize("amount, currency, new_category, spend_date, description", [
    ("456", CurrencyTitle.EUR.value, "after edit spend", "02/09/2025", "spending for update")
])
def test_edit_spending(
        user: tuple[str, str],
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
    with allure.step('Открываем трату для редактирования'):
        spend_row = wait_for_spend_row(main_page, spend.id)
        main_page.click_edit_spend(spend_row)

    spending_page.expected_spend_url(spend.id)

    with allure.step('Вводим сумму траты'):
        spending_page.clear_amount()
        spending_page.fill_amount(amount)

    with allure.step('Выбираем валюту'):
        spending_page.click_currency()
        spending_page.select_currency(currency)

    with allure.step('Изменяем категорию'):
        spending_page.clear_category_input()
        spending_page.fill_category(new_category)

    with allure.step('Изменяем дату траты'):
        spending_page.fill_date(spend_date)

    with allure.step('Изменяем описание'):
        spending_page.clear_description_input()
        spending_page.fill_description(description)

    with allure.step('Нажимаем кнопку «Сохранить»'):
        spending_page.submit_form()

    main_page.expected_url()

    with allure.step('Проверяем уведомление об успешном редактировании'):
        assert main_page.notification.get_notification_text() == "Spending is edited successfully"
        main_page.notification.is_success_notification()

    with allure.step('Сохраняем изменённую трату из UI'):
        edited_spend_row = wait_for_spend_row(main_page=main_page, spend_id=spend.id)

    with allure.step('Получаем изменённую трату через API'):
        api_spend = spend_client.get_spend_by_id(spend.id)
        local_dt = api_spend.spendDate.astimezone(tz.tzlocal())
        date_str = local_dt.strftime("%m/%d/%Y")

    with allure.step('Получаем изменённую трату из БД'):
        db_spend = spend_db.get_spend(spend_id=spend.id)
        db_category = spend_db.get_user_category_by_name(username=user[0], name=new_category)

    with allure.step('Проверяем корректность редактирования траты'):
        with allure.step('Проверяем изменённые данные траты в UI'):
            assert is_text_match_spend_row(
                spend_row_text=edited_spend_row.inner_text(),
                category_name=new_category,
                amount=amount,
                currency=currency,
                description=description,
                spend_date=spend_date
            )
        with allure.step('Проверяем изменённую дату траты в API'):
            assert date_str == spend_date
        with allure.step('Проверяем изменённую категорию траты в API'):
            assert api_spend.category.name == new_category
        with allure.step('Проверяем изменённую валюту траты в API'):
            assert api_spend.currency == currency
        with allure.step('Проверяем изменённую сумму траты в API'):
            assert api_spend.amount == float(amount)
        with allure.step('Проверяем изменённое описание траты в API'):
            assert api_spend.description == description

        with allure.step('Проверяем изменённую сумму траты в БД'):
            assert db_spend.amount == float(amount)
        with allure.step('Проверяем изменённую валюту траты в БД'):
            assert db_spend.currency == currency
        with allure.step('Проверяем изменённую дату траты в БД'):
            assert db_spend.spend_date == datetime.strptime(spend_date, "%m/%d/%Y").date()
        with allure.step('Проверяем изменённое описание траты в БД'):
            assert db_spend.description == description
        with allure.step('Проверяем изменённую категорию траты в БД'):
            assert db_category.name == new_category
