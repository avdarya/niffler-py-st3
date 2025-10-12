import grpc
import pytest

from niffler_tests_python.grpc_pb.internal.pb.niffler_currency_pb2 import CalculateRequest, CurrencyValues
from niffler_tests_python.grpc_pb.internal.pb.niffler_currency_pb2_pbreflect import NifflerCurrencyServiceClient


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
    response = grpc_client.calculate_rate(
        request=CalculateRequest(
            spendCurrency=spend_currency,
            desiredCurrency=desired_currency,
            amount=spend
        )
    )
    assert response.calculatedAmount == expected_result

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
    response = grpc_client.calculate_rate(
        request=CalculateRequest(
            spendCurrency=spend_currency,
            desiredCurrency=desired_currency,
            amount=amount
        )
    )
    assert response.calculatedAmount == expected_result

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
    response = grpc_client.calculate_rate(
        request=CalculateRequest(
            spendCurrency=spend_currency,
            desiredCurrency=desired_currency,
            amount=amount
        )
    )
    print(f'\nRESPONSE: {response.calculatedAmount}')
    assert response.calculatedAmount == expected_result

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
    response = grpc_client.calculate_rate(
        request=CalculateRequest(
            spendCurrency=spend_currency,
            desiredCurrency=desired_currency,
            amount=amount
        )
    )
    assert response.calculatedAmount == expected_result

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
    response = grpc_client.calculate_rate(
        request=CalculateRequest(
            spendCurrency=spend_currency,
            desiredCurrency=desired_currency,
            amount=amount
        )
    )
    assert response.calculatedAmount == expected_result

@pytest.mark.parametrize('spend_currency', [CurrencyValues.UNSPECIFIED])
def test_calculate_rate_with_unspecified_spend_currency(
        grpc_client: NifflerCurrencyServiceClient,
        spend_currency: CurrencyValues,
):
    try:
        _ = grpc_client.calculate_rate(
            request=CalculateRequest(
                spendCurrency=spend_currency,
                desiredCurrency=CurrencyValues.EUR,
                amount=100.00
            )
        )
    except grpc.RpcError as e:
        assert e.code() in (grpc.StatusCode.UNKNOWN, grpc.StatusCode.INTERNAL)
        assert e.details() == 'Application error processing RPC'

@pytest.mark.parametrize('desired_currency', [CurrencyValues.UNSPECIFIED])
def test_calculate_rate_with_unspecified_desired_currency(
        grpc_client: NifflerCurrencyServiceClient,
        desired_currency: CurrencyValues,
):
    try:
        _ = grpc_client.calculate_rate(
            request=CalculateRequest(
                spendCurrency=CurrencyValues.EUR,
                desiredCurrency=desired_currency,
                amount=100.00
            )
        )
    except grpc.RpcError as e:
        assert e.code() in (grpc.StatusCode.UNKNOWN, grpc.StatusCode.INTERNAL)
        assert e.details() == 'Application error processing RPC'

def test_calculate_rate_without_desired_currency(grpc_client: NifflerCurrencyServiceClient):
    try:
        _ = grpc_client.calculate_rate(
            request=CalculateRequest(
                spendCurrency=CurrencyValues.EUR,
                amount=100.00
            )
        )
    except grpc.RpcError as e:
        assert e.code() in (grpc.StatusCode.UNKNOWN, grpc.StatusCode.INTERNAL)
        assert e.details() == 'Application error processing RPC'

def test_calculate_rate_without_spend_currency(grpc_client: NifflerCurrencyServiceClient):
    try:
        _ = grpc_client.calculate_rate(
            request=CalculateRequest(
                desiredCurrency=CurrencyValues.EUR,
                amount=100.00
            )
        )
    except grpc.RpcError as e:
        assert e.code() in (grpc.StatusCode.UNKNOWN, grpc.StatusCode.INTERNAL)
        assert e.details() == 'Application error processing RPC'

@pytest.mark.parametrize('expected_result', [ 0.0 ]
)
def test_calculate_rate_without_amount(
        grpc_client: NifflerCurrencyServiceClient,
        expected_result: float
):
    response = grpc_client.calculate_rate(
            request=CalculateRequest(
                spendCurrency=CurrencyValues.EUR,
                desiredCurrency=CurrencyValues.RUB
            )
        )
    assert response.calculatedAmount == expected_result


