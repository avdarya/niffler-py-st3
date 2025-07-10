import time
from niffler_tests_python.clients.spend_client import SpendApiClient
from niffler_tests_python.model.spend import SpendModel


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
    end_time = time.time() + timeout
    while time.time() < end_time:
        for spend_record in api_response:
            if (
                spend_record.currency == currency and
                spend_record.amount == float(amount) and
                spend_record.description == description and
                # spend_record.spendDate.startswith(spend_date) and
                spend_record.category.name == category_name
            ):
                return spend_record
        time.sleep(interval)
        api_response = spend_client.get_all_spends()

    raise AssertionError(
                f"Не найдена запись с currency={currency}, amount={amount}, "
                f"description={description}, category_name={category_name}, spend_date={spend_date}"
            )