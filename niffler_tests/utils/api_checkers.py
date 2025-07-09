import time

from niffler_tests.clients.spend_client import SpendApiClient


def assert_spend_record_exists(
        api_response: list,
        currency: str,
        amount: str,
        description: str,
        spend_date: str,
        category_name: str,
        spend_client: SpendApiClient,
        timeout: float = 5,
        interval: float = 0.5
):
    end_time = time.time() + timeout
    while time.time() < end_time:
        for record in api_response:
            if (
                record['currency'] == currency and
                record['amount'] == float(amount) and
                record['description'] == description and
                # record['spendDate'].startswith(spend_date) and
                record['category']['name'] == category_name
            ):
                return record
        time.sleep(interval)
        api_response = spend_client.get_all_spends().json()

    raise AssertionError(
                f"Не найдена запись с currency={currency}, amount={amount}, "
                f"description={description}, category_name={category_name}, spend_date={spend_date}"
            )