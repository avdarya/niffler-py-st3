import allure
import pytest

from niffler_tests_python.grpc_pb.internal.pb.niffler_currency_pb2 import CurrencyValues
from niffler_tests_python.grpc_pb.internal.pb.niffler_currency_pb2_pbreflect import NifflerCurrencyServiceClient
from google.protobuf import empty_pb2


@allure.epic("Траты")
@allure.feature("Валюты")
@allure.story("gRPC")
@allure.tag("positive")
@allure.title("Пользователь получает полный список валют через gRPC")
@pytest.mark.parametrize('expected_count', [ 4 ])
def test_get_all_currencies_count(
        grpc_client: NifflerCurrencyServiceClient,
        expected_count: int,
):
    with allure.step("Отправить gRPC-запрос на получение всех валют"):
        response = grpc_client.get_all_currencies(empty_pb2.Empty())

    with allure.step("Проверить, что количество валют в ответе совпадает с ожидаемым"):
        assert len(response.allCurrencies) == 4

@allure.epic("Траты")
@allure.feature("Валюты")
@allure.story("gRPC")
@allure.tag("positive")
@allure.title("Пользователь получает корректные наименования валют через gRPC")
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
    with allure.step("Отправить gRPC-запрос на получение всех валют"):
        response = grpc_client.get_all_currencies(empty_pb2.Empty())
    resp_currencies = {c.currency for c in response.allCurrencies}

    with allure.step("Проверить, что список валют содержит RUB, KZT, EUR и USD"):
        assert set(expected_currency) == resp_currencies

@allure.epic("Траты")
@allure.feature("Валюты")
@allure.story("gRPC")
@allure.tag("positive")
@allure.title("Пользователь получает корректные курсы валют через gRPC")
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
    with allure.step("Отправить gRPC-запрос на получение всех валют и курсов"):
        response = grpc_client.get_all_currencies(empty_pb2.Empty())
    resp_currencies = {c.currency: c.currencyRate for c in response.allCurrencies}

    with allure.step("Проверить корректность курсов валют (RUB, KZT, EUR, USD) в ответе"):
        assert expected_currency_to_rate[CurrencyValues.RUB] == resp_currencies[CurrencyValues.RUB]
        assert expected_currency_to_rate[CurrencyValues.KZT] == resp_currencies[CurrencyValues.KZT]
        assert expected_currency_to_rate[CurrencyValues.EUR] == resp_currencies[CurrencyValues.EUR]
        assert expected_currency_to_rate[CurrencyValues.USD] == resp_currencies[CurrencyValues.USD]
