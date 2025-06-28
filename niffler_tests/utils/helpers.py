import time
from datetime import datetime
from selenium.webdriver.remote.webelement import WebElement
from niffler_tests.clients.category_client import CategoryApiClient
from niffler_tests.web_pages.MainPage import MainPage

def wait_for_category_update_name(
        categories_client: CategoryApiClient,
        category_id: str,
        expected_name: str,
        timeout=5,
        interval=0.5
):
    end_time = time.time() + timeout
    while time.time() < end_time:
        resp = categories_client.get_all_categories()
        if resp.status_code != 200:
            continue

        categories = resp.json()
        for category in categories:
            if category["id"] == category_id and category["name"] == expected_name:
                return category
        time.sleep(interval)

    raise AssertionError(f"Категория {category_id} не обновилась на '{expected_name}' за {timeout} секунд")

def wait_for_category_update_archive(
        categories_client: CategoryApiClient,
        category_id: str,
        expected_archive: bool,
        timeout=5,
        interval=0.5
):
    end_time = time.time() + timeout
    while time.time() < end_time:
        resp = categories_client.get_all_categories()
        if resp.status_code != 200:
            continue

        categories = resp.json()
        for category in categories:
            if category["id"] == category_id and category["archived"] == expected_archive:
                return category
        time.sleep(interval)

    raise AssertionError(f"Категория {category_id} не обновилась на '{expected_archive}' за {timeout} секунд")

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