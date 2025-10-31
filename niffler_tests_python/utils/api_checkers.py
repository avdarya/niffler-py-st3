import time
from datetime import datetime
from niffler_tests_python.clients.spend_client import SpendApiClient
from niffler_tests_python.model.rest_model.spend import SpendModel


def assert_spend_record_exists(
        api_response: list[SpendModel],
        currency: str,
        amount: str,
        description: str,
        spend_date: str,
        category_name: str,
        spend_client: SpendApiClient,
        timeout: float = 5,
        interval: float = 0.5
) -> SpendModel:
    expected_date = datetime.strptime(spend_date, "%m/%d/%Y").date()
    end_time = time.time() + timeout
    while time.time() < end_time:
        for spend_record in api_response:
            print(f'spend_record.spendDate.date()={spend_record.spendDate.date()}')
            print(f'expected_date={expected_date}')
            if (
                spend_record.currency == currency and
                spend_record.amount == float(amount) and
                spend_record.description == description and
                spend_record.spendDate.date() == expected_date and
                spend_record.category.name == category_name
            ):
                return spend_record
        time.sleep(interval)
        api_response = spend_client.get_all_spends()

    raise AssertionError(
                f"Не найдена запись с currency={currency}, amount={amount}, "
                f"description={description}, category_name={category_name}, spend_date={spend_date}"
            )