import time
from datetime import datetime
from typing import Callable
from selenium.webdriver.remote.webelement import WebElement
from niffler_tests_python.clients.category_client import CategoryApiClient
from niffler_tests_python.model.category import CategoryModel
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

def wait_for_spend_row(main_page: MainPage, spend_id: str, timeout=10, interval=0.5) -> WebElement:
    end_time = time.time() + timeout
    while time.time() < end_time:
        spend_row = main_page.get_spend_row(spend_id)
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