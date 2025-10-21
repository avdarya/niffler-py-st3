import math
import allure

import pytest

from niffler_tests_python.clients.graphql_client import GraphQLClient
from niffler_tests_python.clients.spend_client import SpendApiClient
from niffler_tests_python.databases.spend_db import SpendDB
from niffler_tests_python.fixtures.client_fixtures import spend_db
from niffler_tests_python.model.enums.currency_title import CurrencyTitle
from niffler_tests_python.model.enums.period_title import PeriodTitle
from niffler_tests_python.model.spend import SpendModel, SpendModelDB
from niffler_tests_python.utils.graphql_loader import load_graphql_query
from niffler_tests_python.utils.helpers import formated_stat_by_categories, calc_total_stat_by_currency
from niffler_tests_python.utils.marks import TestData


def build_stat_variables(
        stat_currency: CurrencyTitle,
        filter_currency: CurrencyTitle,
        filter_period: PeriodTitle
) -> dict:
    variables = {}
    if stat_currency != CurrencyTitle.ALL:
        variables["statCurrency"] = stat_currency
    if filter_currency != CurrencyTitle.ALL:
        variables["filterCurrency"] = filter_currency
    if filter_period != PeriodTitle.ALL_TIME:
        variables["filterPeriod"] = filter_period
    return variables

@allure.epic("Траты")
@allure.feature("Статистика трат")
@allure.story("GraphQL")
@allure.tag("positive")
@allure.title("Пользователь может получить статистику трат без фильтров и сверить данные с БД")
@TestData.fill_spends
@pytest.mark.parametrize('query_file, default_currency', [
    ('stat_query', CurrencyTitle.RUB)
])
def test_stat_without_filter(
        graphql_client: GraphQLClient,
        user: tuple[str, str],
        spend_db: SpendDB,
        spend_client: SpendApiClient,
        query_file: str,
        default_currency: str
):
    username, _ = user
    with allure.step("Выполнить GraphQL-запрос статистики без фильтров"):
        query = load_graphql_query(query_file)
        response = graphql_client.query_stat(
            query=query,
            variables={}
        )
    with allure.step("Получить траты и категории пользователя из базы данных"):
        db_spends = spend_db.get_spend_by_filter(username=username)
        db_categories = spend_db.get_user_categories(username)
    with allure.step("Рассчитать ожидаемую статистику по данным БД"):
        db_total = calc_total_stat_by_currency(db_spends, default_currency, spend_client)
    with allure.step("Проверить корректность данных статистики из GraphQL и БД"):
        categories = formated_stat_by_categories(response.data.stat.statByCategories)

        assert response.data.stat.total == pytest.approx(db_total, abs=0.02)
        assert response.data.stat.currency == default_currency
        assert len(response.data.stat.statByCategories) == len(db_categories)
        assert categories['sum'] == pytest.approx(db_total, abs=0.02)
        assert categories['currency'] == [default_currency]
        assert sorted(categories['category_name']) == sorted([c.name for c  in db_categories])
        assert categories['first_spend_date'] <= categories['last_spend_date']

@allure.epic("Траты")
@allure.feature("Статистика трат")
@allure.story("GraphQL")
@allure.tag("positive")
@allure.title("Пользователь может получить статистику с фильтрами по валюте и периоду и сверить данные с БД")
@TestData.fill_spends
@pytest.mark.parametrize("query_file, stat_currency, filter_currency, filter_period", [
    ('stat_query', CurrencyTitle.RUB, CurrencyTitle.RUB, PeriodTitle.ALL_TIME),
    ('stat_query', CurrencyTitle.RUB, CurrencyTitle.EUR, PeriodTitle.ALL_TIME),
    ('stat_query', CurrencyTitle.KZT, CurrencyTitle.RUB, PeriodTitle.ALL_TIME),
    ('stat_query', CurrencyTitle.EUR, CurrencyTitle.USD, PeriodTitle.MONTH),
    ('stat_query', CurrencyTitle.RUB, CurrencyTitle.KZT, PeriodTitle.TODAY),
    ('stat_query', CurrencyTitle.USD, CurrencyTitle.ALL, PeriodTitle.WEEK),
    ('stat_query', CurrencyTitle.EUR, CurrencyTitle.RUB, PeriodTitle.ALL_TIME),
])
def test_stat_filters(
        graphql_client: GraphQLClient,
        user: tuple[str, str],
        spend_db: SpendDB,
        spend_client: SpendApiClient,
        query_file: str,
        stat_currency: CurrencyTitle,
        filter_currency: CurrencyTitle,
        filter_period: PeriodTitle
):
    username, _ = user
    with allure.step("Выполнить GraphQL-запрос статистики с фильтрами по валюте и периоду"):
        response = graphql_client.query_stat(
            query=load_graphql_query(query_file),
            variables=build_stat_variables(stat_currency, filter_currency, filter_period)
        )
    with allure.step("Получить траты пользователя из базы данных с применением фильтров"):
        db_spends = spend_db.get_spend_by_filter(username=username, currency=filter_currency, period=filter_period)
    with allure.step("Рассчитать ожидаемую статистику по данным БД"):
        db_total = calc_total_stat_by_currency(db_spends, stat_currency, spend_client)
    with allure.step("Проверить корректность данных статистики между GraphQL и БД"):
        categories = formated_stat_by_categories(response.data.stat.statByCategories)

        db_category_ids = set(spend.category_id for spend in db_spends)
        db_categories = spend_db.get_categories_by_id(db_category_ids)
        db_category_names = set(c.name for c in db_categories)

        assert response.data.stat.total == pytest.approx(db_total, abs=0.02)
        assert response.data.stat.currency == stat_currency
        assert len(response.data.stat.statByCategories) == len(db_category_names)
        assert categories['sum'] == pytest.approx(db_total, abs=0.02)
        assert categories['currency'] == [stat_currency]
        assert sorted(categories['category_name']) == sorted(db_category_names)
        assert categories['first_spend_date'] <= categories['last_spend_date']

@allure.epic("Траты")
@allure.feature("Статистика трат")
@allure.story("GraphQL")
@allure.tag("positive")
@allure.title("Пользователь без трат получает пустую статистику в GraphQL")
@pytest.mark.parametrize("query_file, expected_total, expected_currency", [
    ('stat_query', 0.0, CurrencyTitle.RUB)
])
def test_stat_empty_spend(
        graphql_client: GraphQLClient,
        user: tuple[str, str],
        spend_db: SpendDB,
        spend_client: SpendApiClient,
        query_file: str,
        expected_total: float,
        expected_currency: CurrencyTitle
):
    username, _ = user
    with allure.step("Выполнить GraphQL-запрос статистики без трат"):
        response = graphql_client.query_stat(
            query=load_graphql_query(query_file),
            variables={}
        )
    with allure.step("Проверить, что сумма, валюта и категории в ответе соответствуют ожидаемым значениям"):
        assert response.data.stat.total == expected_total
        assert response.data.stat.currency == expected_currency
        assert len(response.data.stat.statByCategories) == 0

@allure.epic("Траты")
@allure.feature("Статистика трат")
@allure.story("GraphQL")
@allure.tag("positive")
@allure.title("Пользователь получает статистику с учётом архивных категорий и сверяет её с БД")
@TestData.filled_spends_contains_archived_category
@pytest.mark.parametrize("query_file, stat_currency, filter_currency, filter_period, expected_archive", [
    ('stat_query', CurrencyTitle.RUB, CurrencyTitle.ALL, PeriodTitle.MONTH, 'Archived')
])
def test_stat_contains_archived_category(
        graphql_client: GraphQLClient,
        user: tuple[str, str],
        spend_db: SpendDB,
        spend_client: SpendApiClient,
        query_file: str,
        stat_currency: CurrencyTitle,
        filter_currency: CurrencyTitle,
        filter_period: PeriodTitle,
        expected_archive: str
):
    username, _ = user
    with allure.step("Выполнить GraphQL-запрос статистики с архивными категориями"):
        response = graphql_client.query_stat(
            query=load_graphql_query(query_file),
            variables=build_stat_variables(stat_currency, filter_currency, filter_period)
        )
    with allure.step("Получить траты и категории пользователя из базы данных"):
        db_spends = spend_db.get_spend_by_filter(username=username, currency=filter_currency, period=filter_period)
        db_category_ids = set(spend.category_id for spend in db_spends)
        db_active_categories = spend_db.get_active_categories_by_id(db_category_ids)
        db_active_category_names = set(c.name for c in db_active_categories)
    with allure.step("Рассчитать ожидаемую статистику по данным БД"):
        db_total = calc_total_stat_by_currency(db_spends, stat_currency, spend_client)
    with allure.step("Проверить корректность данных статистики между GraphQL и БД, включая архивные категории"):
        categories = formated_stat_by_categories(response.data.stat.statByCategories)

        assert response.data.stat.total == pytest.approx(db_total, abs=0.02)
        assert response.data.stat.currency == stat_currency
        assert categories['is_contains_archived'] is True
        assert len(response.data.stat.statByCategories) - 1 == len(db_active_category_names)
        assert categories['sum'] == pytest.approx(db_total, abs=0.02)
        assert categories['currency'] == [stat_currency]
        assert sorted(categories['category_name']) == sorted(db_active_category_names)
        assert categories['first_spend_date'] <= categories['last_spend_date']