from datetime import datetime

import allure
import pytest

from niffler_tests_python.clients.spend_client import SpendApiClient
from niffler_tests_python.databases.spend_db import SpendDB
from niffler_tests_python.model.rest_model.category import CategoryModel
from niffler_tests_python.model.enums.currency_title import CurrencyTitle
from niffler_tests_python.utils.api_checkers import assert_spend_record_exists
from niffler_tests_python.utils.helpers import wait_for_spend_row, is_text_match_spend_row
from niffler_tests_python.utils.marks import TestData, Pages
from niffler_tests_python.web_pages.MainPage import MainPage
from niffler_tests_python.web_pages.SpendingPage import SpendingPage
from niffler_tests_python.web_pages.components.HeaderComponent import HeaderComponent


@allure.epic("Траты")
@allure.feature("Создание траты")
@allure.story("UI")
@allure.tag("positive")
@allure.title("Создание траты — проверка записи в БД и отображения на главной странице")
@Pages.go_to_main_page
@TestData.category("add spend")
@pytest.mark.parametrize("amount, currency, spend_date, description", [
    ("10.01", CurrencyTitle.RUB.value, "12/09/2024", "test add spending"),
    ("501", CurrencyTitle.KZT.value, "01/15/2025", "test add spending"),
    ("0.01", CurrencyTitle.EUR.value, "04/09/2025", "test add spending"),
    ("3", CurrencyTitle.USD.value, "06/21/2025", "test add spending")
])
def test_add_spending(
        user: tuple[str, str],
        main_page: MainPage,
        header: HeaderComponent,
        spending_page: SpendingPage,
        spend_client: SpendApiClient,
        category: CategoryModel,
        spend_db: SpendDB,
        cleanup_spends: None,
        amount: str,
        currency: str,
        spend_date: str,
        description: str,
):
    with allure.step('Нажимаем кнопку «Добавить трату»'):
        header.click_new_spending()

    spending_page.expected_url()

    with allure.step('Получаем количество трат до добавления'):
        before_spending = spend_client.get_all_spends()
        before_spending_count = len(before_spending)

    with allure.step('Вводим сумму'):
        spending_page.clear_amount()
        spending_page.fill_amount(amount)

    with allure.step('Выбираем валюту'):
        spending_page.click_currency()
        spending_page.select_currency(currency)

    with allure.step('Выбираем категорию'):
        category_name = category.name
        spending_page.fill_category(category_name)

    with allure.step('Вводим дату'):
        spending_page.fill_date(spend_date)

    with allure.step('Вводим описание'):
        spending_page.fill_description(description)

    with allure.step('Нажимаем кнопку «Добавить»'):
        spending_page.submit_form()

    main_page.expected_url()

    with allure.step('Проверяем уведомление об успешном создании траты'):
        main_page.notification.is_success_notification()
        assert main_page.notification.get_notification_text() == 'New spending is successfully created'

    with allure.step('Получаем количество трат после добавления'):
        after_spending = spend_client.get_all_spends()
        after_spending_count = len(after_spending)
        with allure.step('Проверяем, что количество трат увеличилось на 1'):
            assert before_spending_count == after_spending_count - 1

    with allure.step('Получаем добавленную трату через API'):
        api_spend = assert_spend_record_exists(
            api_response=after_spending,
            currency=currency,
            amount=amount,
            spend_date=spend_date,
            description=description,
            category_name=category.name,
            spend_client=spend_client,
        )

    with allure.step('Находим добавленную трату на странице'):
        spend_row = wait_for_spend_row(main_page=main_page, spend_id=api_spend.id)

    with allure.step('Получаем данные добавленной траты из БД'):
        db_spend = spend_db.get_spend(api_spend.id)
        db_category = spend_db.get_user_category_by_name(user[0], category_name)

    with allure.step('Проверяем корректность добавления траты'):
        with allure.step('Проверяем отображение добавленной траты в UI'):
            assert spend_row is not None
            assert is_text_match_spend_row(
                spend_row_text=spend_row.inner_text(),
                category_name=category.name,
                amount=amount,
                currency=currency,
                description=description,
                spend_date=spend_date
            )
        with allure.step('Проверяем сумму в БД'):
            assert db_spend.amount == float(amount)
        with allure.step('Проверяем валюту в БД'):
            assert db_spend.currency == currency
        with allure.step('Проверяем дату в БД'):
            assert db_spend.spend_date == datetime.strptime(spend_date, "%m/%d/%Y").date()
        with allure.step('Проверяем описание в БД'):
            assert db_spend.description == description
        with allure.step('Проверяем категорию в БД'):
            assert db_category.name == category_name
