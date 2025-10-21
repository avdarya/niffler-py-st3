import time
import base64, json
from datetime import datetime
from typing import Callable

from playwright.sync_api import Locator
from niffler_tests_python.clients.category_client import CategoryApiClient
from niffler_tests_python.clients.spend_client import SpendApiClient
from niffler_tests_python.model.category import CategoryModel
from niffler_tests_python.model.enums.currency_title import CurrencyTitle
from niffler_tests_python.model.spend import SpendModelDB
from niffler_tests_python.model.stat import StatByCategoryGqlResponse
from niffler_tests_python.web_pages.MainPage import MainPage


def wait_for_api_condition(
        get_items_fn: Callable,
        condition_fn: Callable,
        timeout: float = 5,
        interval: float = 0.5,
):
    end_time = time.time() + timeout
    while time.time() < end_time:
        items = get_items_fn()
        for item in items:
            if condition_fn(item):
                return item
        time.sleep(interval)
    raise AssertionError('Condition was not met within allowed time')

def wait_for_category_update_name(
        category_client: CategoryApiClient,
        category_id: str,
        expected_name: str,
        timeout : float =5,
        interval: float =0.5
):
    return wait_for_api_condition(
        lambda: fetch_all_categories(category_client),
        category_has_name(category_id, expected_name),
        timeout=timeout,
        interval=interval,
    )

def wait_for_category_update_archive(
        category_client: CategoryApiClient,
        category_id: str,
        expected_archive: bool,
        timeout: float =5,
        interval: float =0.5
):
    return wait_for_api_condition(
        lambda: fetch_all_categories(category_client),
        category_has_archive_state(category_id, expected_archive),
        timeout=timeout,
        interval=interval,
    )

def is_text_match_spend_row(
        spend_row_text: str,
        category_name: str,
        amount: str,
        currency: str,
        description: str | None,
        spend_date: str
) -> bool:
    date_obj = datetime.strptime(spend_date,  "%m/%d/%Y")
    formatted_date = date_obj.strftime("%b %d, %Y")

    currency_symbols = {
        "RUB": "₽",
        "USD": "$",
        "EUR": "€",
        "KZT": "₸",
    }
    amount_with_symbol = f"{amount} {currency_symbols.get(currency, '')}"

    if (
            category_name in spend_row_text and
            amount_with_symbol in spend_row_text and
            (description in spend_row_text or not description) and
            formatted_date in spend_row_text
    ):
        return True
    else:
        return False

def wait_for_spend_row(main_page: MainPage, spend_id: str, timeout=10, interval=0.5) -> Locator:
    end_time = time.time() + timeout
    while time.time() < end_time:
        spend_row = main_page.get_spend_row_by_id(spend_id)
        if spend_row is not None:
            return spend_row
        time.sleep(interval)
    raise AssertionError(f"Spend row with ID {spend_id} не появился в UI за {timeout} секунд")

def fetch_all_categories(category_client: CategoryApiClient) -> list[CategoryModel]:
    return category_client.get_all_categories()

def category_has_name(category_id: str, expected_name: str) -> Callable[[CategoryModel], bool]:
    def predicate(category: CategoryModel) -> bool:
        return category.id == category_id and category.name == expected_name
    return predicate

def category_has_archive_state(category_id: str, expected_archive: bool) -> Callable[[CategoryModel], bool]:
    def predicate(category: CategoryModel) -> bool:
        return category.id == category_id and category.archived == expected_archive
    return predicate

def get_category_by_name(category_name: str, category_client: CategoryApiClient) -> CategoryModel:
    all_categories = category_client.get_all_categories()
    for category in all_categories:
        if category.name == category_name:
            return category
    raise AssertionError(f"Category with name {category_name} not found")

def decode_jwt_payload(token_payload_part: str) -> dict:
    try:
        token_payload_part += '=' * (-len(token_payload_part) % 4)
        decoded_payload =base64.urlsafe_b64decode(token_payload_part)
        return json.loads(decoded_payload)
    except ValueError:
        raise ValueError('Invalid JWT format')

def calc_total_stat_by_currency(
        spends: list[SpendModelDB],
        stat_currency: str,
        spend_api_client: SpendApiClient
) -> float:
    total = 0.0
    all_currencies = spend_api_client.get_all_currencies()
    currency_by_rate = {currency.currency: currency.currencyRate for currency in all_currencies}
    for spend in spends:
        spend_rate = currency_by_rate.get(spend.currency)
        stat_rate = currency_by_rate.get(stat_currency)

        if spend_rate is None or stat_rate is None:
            raise ValueError(f"Missing rate for {spend.currency} or {stat_currency}")

        amount_in_stat_currency = spend.amount * spend_rate / stat_rate
        total += amount_in_stat_currency

    return total


def formated_stat_by_categories (stat_by_category: list[StatByCategoryGqlResponse]) -> dict:
    sums = 0.0
    currency = set()
    category_name = set()
    first_spend_date = None
    last_spend_date = None
    is_contains_archived = False
    for category in stat_by_category:
        sums += category.sum
        currency.add(category.currency)
        if category.categoryName == 'Archived':
            is_contains_archived = True
        else:
            category_name.add(category.categoryName)
        if first_spend_date is None or category.firstSpendDate < first_spend_date:
            first_spend_date = category.firstSpendDate
        if last_spend_date is None or category.lastSpendDate > last_spend_date:
            last_spend_date = category.lastSpendDate
    return {
        'sum': sums,
        'currency': list(currency),
        'category_name': list(category_name),
        'is_contains_archived': is_contains_archived,
        'first_spend_date': first_spend_date,
        'last_spend_date': last_spend_date,
    }
