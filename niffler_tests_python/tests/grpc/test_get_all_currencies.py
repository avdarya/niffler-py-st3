import allure
import pytest

from niffler_tests_python.grpc_pb.internal.pb.niffler_currency_pb2 import CurrencyValues
from niffler_tests_python.grpc_pb.internal.pb.niffler_currency_pb2_pbreflect import NifflerCurrencyServiceClient
from google.protobuf import empty_pb2


@pytest.mark.parametrize('expected_count', [ 4 ])
def test_get_all_currencies_count(
        grpc_client: NifflerCurrencyServiceClient,
        expected_count: int,
):
    response = grpc_client.get_all_currencies(empty_pb2.Empty())

    with allure.step('Проверка количества валют в ответе'):
        assert len(response.allCurrencies) == 4

@pytest.mark.parametrize('expected_currency', [
    {
        CurrencyValues.RUB,
        CurrencyValues.KZT,
        CurrencyValues.EUR,
        CurrencyValues.USD
    }
])
def test_get_all_currencies_correct_titles(
        grpc_client: NifflerCurrencyServiceClient,
        expected_currency: dict,
):
    response = grpc_client.get_all_currencies(empty_pb2.Empty())
    resp_currencies = {c.currency for c in response.allCurrencies}

    with allure.step('Проверка наименований валют в ответе'):
        assert set(expected_currency) == resp_currencies

@pytest.mark.parametrize('expected_currency_to_rate', [
    {
        CurrencyValues.RUB: 0.015,
        CurrencyValues.KZT: 0.0021,
        CurrencyValues.EUR: 1.08,
        CurrencyValues.USD: 1,
    }
])
def test_get_all_currencies_correct_rates(
        grpc_client: NifflerCurrencyServiceClient,
        expected_currency_to_rate: dict[CurrencyValues, float],
):
    response = grpc_client.get_all_currencies(empty_pb2.Empty())
    resp_currencies = {c.currency: c.currencyRate for c in response.allCurrencies}

    with allure.step('Проверка курса RUB в ответе'):
        assert expected_currency_to_rate[CurrencyValues.RUB] == resp_currencies[CurrencyValues.RUB]

    with allure.step('Проверка курса KZT в ответе'):
        assert expected_currency_to_rate[CurrencyValues.KZT] == resp_currencies[CurrencyValues.KZT]

    with allure.step('Проверка курса EUR в ответе'):
        assert expected_currency_to_rate[CurrencyValues.EUR] == resp_currencies[CurrencyValues.EUR]

    with allure.step('Проверка курса USD в ответе'):
        assert expected_currency_to_rate[CurrencyValues.USD] == resp_currencies[CurrencyValues.USD]


