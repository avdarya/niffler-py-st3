import allure
import pytest
from niffler_tests_python.clients.spend_client import SpendApiClient
from niffler_tests_python.model.enums.currency_title import CurrencyTitle
from niffler_tests_python.model.enums.period_title import PeriodTitle
from niffler_tests_python.model.rest_model.spend import SpendModelAdd, SpendModel
from niffler_tests_python.utils.marks import TestData
from niffler_tests_python.web_pages.MainPage import MainPage


@allure.epic("Траты")
@allure.feature("Поиск трат")
@allure.story("UI")
@allure.tag("positive")
@allure.title("Поиск трат по описанию")
@TestData.fill_spends
@TestData.spend(SpendModelAdd(
    amount = 8989.05,
    description = "test search spend by description",
    currency = CurrencyTitle.RUB.value,
    spendDate = "2025-06-27",
    category = {"name": "category for search desc"}
))
def test_search_spend_by_description(spend: SpendModel, main_page: MainPage, spend_client: SpendApiClient):
    description = spend.description

    with allure.step('Переходим на главную страницу'):
        main_page.navigate()

    with allure.step('Вводим запрос поиска по описанию'):
        main_page.enter_search_query(description)

    with allure.step('Получаем данные через API по описанию'):
        api_search_query = spend_client.get_all_spends_v2(search_query=description)
        api_spend_ids = [spend_item["id"] for spend_item in api_search_query["content"]]

    with allure.step('Получаем идентификаторы трат в UI после поиска'):
        search_spend_ids = main_page.get_spend_ids()

    with allure.step('Получаем введённый текст поиска'):
        search_input_text = main_page.get_search_query_input()

    with allure.step('Сравниваем результаты UI и API'):
        with allure.step('Проверяем, что введённый текст совпадает с запросом'):
            assert search_input_text == description
        with allure.step('Проверяем, что количество трат из API совпадает с UI'):
            assert len(api_spend_ids) == len(search_spend_ids)
        with allure.step('Проверяем, что идентификаторы трат из API совпадают с UI'):
            assert api_spend_ids == search_spend_ids

@allure.epic("Траты")
@allure.feature("Поиск трат")
@allure.story("UI")
@allure.tag("positive")
@allure.title("Поиск трат по категории")
@TestData.fill_spends
@TestData.spend(SpendModelAdd(
    amount = 8989.05,
    description = "test search spend by category",
    currency = CurrencyTitle.RUB.value,
    spendDate = "2025-06-27",
    category = {"name": "category for search category"}
))
def test_search_spend_by_category(spend: SpendModel, main_page: MainPage, spend_client: SpendApiClient):
    category_name = spend.category.name

    with allure.step('Переходим на главную страницу'):
        main_page.navigate()

    with allure.step('Выбираем категорию'):
        main_page.enter_search_query(category_name)

    with allure.step('Получаем данные через API по категории'):
        api_search_query = spend_client.get_all_spends_v2(search_query=category_name)
        api_spend_ids = [spend_item["id"] for spend_item in api_search_query["content"]]

    with allure.step('Получаем идентификаторы трат в UI после поиска'):
        search_spend_ids = main_page.get_spend_ids()

    with allure.step('Получаем введённый текст поиска'):
        search_input_text = main_page.get_search_query_input()

    with allure.step('Сравниваем результаты UI и API'):
        with allure.step('Проверяем, что введённый текст совпадает с категорией'):
            assert search_input_text == category_name
        with allure.step('Проверяем, что количество трат из API совпадает с UI'):
            assert len(api_spend_ids) == len(search_spend_ids)
        with allure.step('Проверяем, что идентификаторы трат из API совпадают с UI'):
            assert set(api_spend_ids) == set(search_spend_ids)

@allure.epic("Траты")
@allure.feature("Поиск трат")
@allure.story("UI")
@allure.tag("positive")
@allure.title("Поиск трат по периоду")
@TestData.fill_spends
@pytest.mark.parametrize("custom_date_spend", [
    {
        "amount": 8989.05,
        "description": "test search spend by MONTH",
        "currency": CurrencyTitle.RUB.value,
        "spendDate": PeriodTitle.MONTH.value,
        "category": {"name": "category for search period"}
    },
    {
        "amount": 8989.05,
        "description": "test search spend by WEEK",
        "currency": CurrencyTitle.RUB.value,
        "spendDate": PeriodTitle.WEEK.value,
        "category": {"name": "category for search period"}
    },
    {
        "amount": 8989.05,
        "description": "test search spend by TODAY",
        "currency": CurrencyTitle.RUB.value,
        "spendDate": PeriodTitle.TODAY.value,
        "category": {"name": "category for search period"}
    }
], indirect=True)
def test_search_spend_by_period(
        custom_date_spend: tuple[SpendModel, dict[str, str]],
        main_page: MainPage,
        spend_client: SpendApiClient
):
    added_spend, period_dict = custom_date_spend
    period = period_dict["period"]

    with allure.step('Переходим на главную страницу'):
        main_page.navigate()

    with allure.step('Выбираем период'):
        main_page.click_period_field()
        main_page.select_period_value(period)

    with allure.step('Получаем данные через API по периоду'):
        api_search = spend_client.get_all_spends_v2(filter_period=period)
        api_spend_ids = [spend_item["id"] for spend_item in api_search["content"]]

    with allure.step('Получаем идентификаторы трат в UI после поиска'):
        search_spend_ids = main_page.get_spend_ids()

    with allure.step('Получаем выбранный период в UI'):
        period_input_text = main_page.get_period_input()

    with allure.step('Сравниваем результаты UI и API'):
        with allure.step('Проверяем, что выбранный период совпадает'):
            assert period_input_text == period
        with allure.step('Проверяем, что количество трат из API совпадает с UI'):
            assert len(api_spend_ids) == len(search_spend_ids)
        with allure.step('Проверяем, что идентификаторы трат из API совпадают с UI'):
            assert set(api_spend_ids) == set(search_spend_ids)

@allure.epic("Траты")
@allure.feature("Поиск трат")
@allure.story("UI")
@allure.tag("positive")
@allure.title("Поиск трат по валюте")
@TestData.fill_spends
@pytest.mark.parametrize("currency", [CurrencyTitle.RUB.value, CurrencyTitle.KZT.value, CurrencyTitle.EUR.value, CurrencyTitle.USD.value])
def test_search_spend_by_currency(
        main_page: MainPage,
        spend_client: SpendApiClient,
        currency: str
):
    with allure.step('Переходим на главную страницу'):
        main_page.navigate()

    with allure.step('Выбираем валюту'):
        main_page.click_currency_field()
        main_page.select_currency_value(currency)

    with allure.step('Получаем данные через API по валюте'):
        api_search = spend_client.get_all_spends_v2(filter_currency=currency)
        api_spend_ids = [spend_item["id"] for spend_item in api_search["content"]]

    with allure.step('Получаем идентификаторы трат в UI после поиска'):
        search_spend_ids = main_page.get_spend_ids()

    with allure.step('Получаем выбранную валюту в UI'):
        currency_input_text = main_page.get_currency_input()

    with allure.step('Сравниваем результаты UI и API'):
        with allure.step('Проверяем, что выбранная валюта совпадает'):
            assert currency_input_text == currency
        with allure.step('Проверяем, что количество трат из API совпадает с UI'):
            assert len(api_spend_ids) == len(search_spend_ids)
        with allure.step('Проверяем, что идентификаторы трат из API совпадают с UI'):
            assert api_spend_ids == search_spend_ids