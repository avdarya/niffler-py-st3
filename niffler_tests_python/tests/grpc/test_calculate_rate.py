import grpc
import pytest
import allure

from niffler_tests_python.grpc_pb.internal.pb.niffler_currency_pb2 import CalculateRequest, CurrencyValues
from niffler_tests_python.grpc_pb.internal.pb.niffler_currency_pb2_pbreflect import NifflerCurrencyServiceClient


@allure.epic("Траты")
@allure.feature("Расчет валютного курса")
@allure.story("gRPC")
@allure.tag("positive")
@allure.title("Проверка корректного расчета валютного курса при различных комбинациях валют")
@pytest.mark.parametrize('spend, spend_currency, desired_currency, expected_result', [
    (100.0, CurrencyValues.USD, CurrencyValues.RUB, 6666.67),
    (100.0, CurrencyValues.RUB, CurrencyValues.USD, 1.5),
    (100.0, CurrencyValues.EUR, CurrencyValues.RUB, 7200.0),
    (100.0, CurrencyValues.RUB, CurrencyValues.EUR, 1.39),
    (100.0, CurrencyValues.USD, CurrencyValues.USD, 100.0),
    (100.0, CurrencyValues.KZT, CurrencyValues.USD, 0.21),
    (100.0, CurrencyValues.USD, CurrencyValues.KZT, 47619.05),
    ]
)
def test_currency_conversion(
        grpc_client: NifflerCurrencyServiceClient,
        spend: float,
        spend_currency: CurrencyValues,
        desired_currency: CurrencyValues,
        expected_result: float
):
    with allure.step("Отправить gRPC-запрос на расчет валютного курса"):
        response = grpc_client.calculate_rate(
            request=CalculateRequest(
                spendCurrency=spend_currency,
                desiredCurrency=desired_currency,
                amount=spend
            )
        )
    with allure.step("Проверить корректность рассчитанного значения"):
        assert response.calculatedAmount == expected_result

@allure.epic("Траты")
@allure.feature("Расчет валютного курса")
@allure.story("gRPC")
@allure.tag("positive")
@allure.title("Проверка корректного расчета валютного курса при больших значениях валют")
@pytest.mark.parametrize('amount, expected_result, spend_currency, desired_currency', [
    (1000000, 6.666666667e+07, CurrencyValues.USD, CurrencyValues.RUB),
])
def test_calculate_rate_with_large_amount(
        grpc_client: NifflerCurrencyServiceClient,
        amount: float,
        expected_result: float,
        spend_currency: CurrencyValues,
        desired_currency: CurrencyValues
):
    with allure.step("Сформировать gRPC-запрос"):
        request = CalculateRequest(
            spendCurrency=spend_currency,
            desiredCurrency=desired_currency,
            amount=amount
        )
    with allure.step("Отправить запрос и получить ответ"):
        response = grpc_client.calculate_rate(request=request)
    with allure.step("Проверить тело ответа и код статуса"):
        assert response.calculatedAmount == expected_result

@allure.epic("Траты")
@allure.feature("Расчет валютного курса")
@allure.story("gRPC")
@allure.tag("positive")
@allure.title("Проверка корректного расчета валютного курса при значениях валют меньше единицы")
@pytest.mark.parametrize('amount, expected_result, spend_currency, desired_currency', [
    (0.01, 0.0, CurrencyValues.RUB, CurrencyValues.EUR),
])
def test_calculate_rate_with_less_one_amount(
        grpc_client: NifflerCurrencyServiceClient,
        amount: float,
        expected_result: float,
        spend_currency: CurrencyValues,
        desired_currency: CurrencyValues
):
    with allure.step("Сформировать gRPC-запрос"):
        request = CalculateRequest(
            spendCurrency=spend_currency,
            desiredCurrency=desired_currency,
            amount=amount
        )
    with allure.step("Отправить запрос и получить ответ"):
        response = grpc_client.calculate_rate(request=request)
    with allure.step("Проверить тело ответа и код статуса"):
        assert response.calculatedAmount == expected_result

@allure.epic("Траты")
@allure.feature("Расчет валютного курса")
@allure.story("gRPC")
@allure.tag("negative")
@allure.title("Проверка расчета при нулевой сумме")
@pytest.mark.parametrize('amount, expected_result, spend_currency, desired_currency', [
    (0, 0.0, CurrencyValues.USD, CurrencyValues.RUB),
])
def test_calculate_rate_with_zero_amount(
        grpc_client: NifflerCurrencyServiceClient,
        amount: float,
        expected_result: float,
        spend_currency: CurrencyValues,
        desired_currency: CurrencyValues
):
    with allure.step("Сформировать gRPC-запрос"):
        request = CalculateRequest(
            spendCurrency=spend_currency,
            desiredCurrency=desired_currency,
            amount=amount
        )
    with allure.step("Отправить запрос и получить ответ"):
        response = grpc_client.calculate_rate(request=request)
    with allure.step("Проверить тело ответа и код статуса"):
        assert response.calculatedAmount == expected_result

@allure.epic("Траты")
@allure.feature("Расчет валютного курса")
@allure.story("gRPC")
@allure.tag("negative")
@allure.title("Проверка расчета при отрицательной сумме")
@pytest.mark.parametrize('amount, expected_result, spend_currency, desired_currency', [
    (-1, -66.67, CurrencyValues.USD, CurrencyValues.RUB)
])
def test_calculate_rate_with_negative_amount(
        grpc_client: NifflerCurrencyServiceClient,
        amount: float,
        expected_result: float,
        spend_currency: CurrencyValues,
        desired_currency: CurrencyValues
):
    with allure.step("Сформировать gRPC-запрос"):
        request = CalculateRequest(
            spendCurrency=spend_currency,
            desiredCurrency=desired_currency,
            amount=amount
        )
    with allure.step("Отправить запрос и получить ответ"):
        response = grpc_client.calculate_rate(request=request)
    with allure.step("Проверить тело ответа и код статуса"):
        assert response.calculatedAmount == expected_result

@allure.epic("Траты")
@allure.feature("Расчет валютного курса")
@allure.story("gRPC")
@allure.tag("negative")
@allure.title("Ошибка при неуказанной валюте траты")
@pytest.mark.parametrize('spend_currency', [CurrencyValues.UNSPECIFIED])
def test_calculate_rate_with_unspecified_spend_currency(
        grpc_client: NifflerCurrencyServiceClient,
        spend_currency: CurrencyValues,
):
    with allure.step("Сформировать gRPC-запрос"):
        request = CalculateRequest(
            spendCurrency=spend_currency,
            desiredCurrency=CurrencyValues.EUR,
            amount=100.00
        )
    with allure.step("Отправить запрос и получить ответ"):
        try:
            _ = grpc_client.calculate_rate(request=request)
        except grpc.RpcError as e:
            with allure.step("Проверить тело ответа и код статуса"):
                assert e.code() in (grpc.StatusCode.UNKNOWN, grpc.StatusCode.INTERNAL)
                assert e.details() == 'Application error processing RPC'

@allure.epic("Траты")
@allure.feature("Расчет валютного курса")
@allure.story("gRPC")
@allure.tag("negative")
@allure.title("Ошибка при неуказанной целевой валюте")
@pytest.mark.parametrize('desired_currency', [CurrencyValues.UNSPECIFIED])
def test_calculate_rate_with_unspecified_desired_currency(
        grpc_client: NifflerCurrencyServiceClient,
        desired_currency: CurrencyValues,
):
    with allure.step("Сформировать gRPC-запрос"):
        request = CalculateRequest(
            spendCurrency=CurrencyValues.EUR,
            desiredCurrency=desired_currency,
            amount=100.00
        )
    with allure.step("Отправить запрос и получить ответ"):
        try:
            _ = grpc_client.calculate_rate(request=request)
        except grpc.RpcError as e:
            with allure.step("Проверить тело ответа и код статуса"):
                assert e.code() in (grpc.StatusCode.UNKNOWN, grpc.StatusCode.INTERNAL)
                assert e.details() == 'Application error processing RPC'

@allure.epic("Траты")
@allure.feature("Расчет валютного курса")
@allure.story("gRPC")
@allure.tag("negative")
@allure.title("Ошибка при отсутствии обязательного поля целевой валюты")
def test_calculate_rate_without_desired_currency(grpc_client: NifflerCurrencyServiceClient):
    with allure.step("Сформировать gRPC-запрос"):
        request = CalculateRequest(
            spendCurrency=CurrencyValues.EUR,
            amount=100.00
        )
    with allure.step("Отправить запрос и получить ответ"):
        try:
            _ = grpc_client.calculate_rate(request=request)
        except grpc.RpcError as e:
            with allure.step("Проверить тело ответа и код статуса"):
                assert e.code() in (grpc.StatusCode.UNKNOWN, grpc.StatusCode.INTERNAL)
                assert e.details() == 'Application error processing RPC'

@allure.epic("Траты")
@allure.feature("Расчет валютного курса")
@allure.story("gRPC")
@allure.tag("negative")
@allure.title("Ошибка при отсутствии обязательного поля валюты траты")
def test_calculate_rate_without_spend_currency(grpc_client: NifflerCurrencyServiceClient):
    with allure.step("Сформировать gRPC-запрос"):
        request = CalculateRequest(
            desiredCurrency=CurrencyValues.EUR,
            amount=100.00
        )
    with allure.step("Отправить запрос и получить ответ"):
        try:
            _ = grpc_client.calculate_rate(request=request)
        except grpc.RpcError as e:
            with allure.step("Проверить тело ответа и код статуса"):
                assert e.code() in (grpc.StatusCode.UNKNOWN, grpc.StatusCode.INTERNAL)
                assert e.details() == 'Application error processing RPC'

@allure.epic("Траты")
@allure.feature("Расчет валютного курса")
@allure.story("gRPC")
@allure.tag("negative")
@allure.title("Ошибка при отсутствии обязательного поля сумма траты")
@pytest.mark.parametrize('expected_result', [ 0.0 ]
)
def test_calculate_rate_without_amount(
        grpc_client: NifflerCurrencyServiceClient,
        expected_result: float
):
    with allure.step("Сформировать gRPC-запрос"):
        request = CalculateRequest(
            spendCurrency=CurrencyValues.EUR,
            desiredCurrency=CurrencyValues.RUB
        )
    with allure.step("Отправить запрос и получить ответ"):
        response = grpc_client.calculate_rate(request=request)
    with allure.step("Проверить тело ответа и код статуса"):
        assert response.calculatedAmount == expected_result
