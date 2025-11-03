from datetime import timedelta

from niffler_tests_python.model.rest_model.currency import CurrencyModel
from niffler_tests_python.model.rest_model.error_response import ErrorResponseModel
from niffler_tests_python.model.rest_model.spend import SpendModel, SpendModelAdd, SpendModelEdit
from niffler_tests_python.utils.sessions import BaseSession


class SpendApiClient:

    session: BaseSession

    def __init__(self, session: BaseSession):
        self.session = session

    def get_all_spends(self, filter_currency: str = None, filter_period: str = None) -> list[SpendModel]:
        response = self.session.get(
            "/api/spends/all",
            params={"filterCurrency": filter_currency, "filterPeriod": filter_period}
        )
        spends = [SpendModel.model_validate(item) for item in response.json()]
        updated_spends = [spend.model_copy(update={'spendDate': spend.spendDate + timedelta(hours=3)}) for spend in spends]
        return updated_spends

    def get_all_currencies(self) -> list[CurrencyModel]:
        response = self.session.get("/api/currencies/all")
        currencies = [CurrencyModel.model_validate(currency) for currency in response.json()]
        return currencies

    def get_spend_by_id(self, spend_id: str) -> SpendModel:
        response = self.session.get(f"/api/spends/{spend_id}")
        spend = SpendModel.model_validate(response.json())
        updated_spend = spend.model_copy(update={'spendDate': spend.spendDate + timedelta(hours=3)})
        return updated_spend

    def add_spend(self, spend: SpendModelAdd) -> SpendModel:
        response = self.session.post(
            "/api/spends/add",
            json=spend.model_dump()
        )
        return SpendModel.model_validate(response.json())

    def edit_spend(self, spend: SpendModelEdit) -> SpendModel:
        response = self.session.patch(
            "/api/spends/edit",
            json=spend.model_dump()
        )
        return SpendModel.model_validate(response.json())

    def delete_spend(self, ids: list[str]) -> None:
        self.session.delete(
            "/api/spends/remove",
            params={"ids": ",".join(ids)}
        )

    def get_all_spends_v2(
            self,
            page: int = 0,
            search_query: str = None,
            filter_period: str = None,
            filter_currency: str = None
    ) -> dict:
        params = {
            "page": page,
            "searchQuery": search_query,
            "filterPeriod": filter_period,
            "filterCurrency": filter_currency
        }
        response =  self.session.get(
            "/api/v2/spends/all",
            params=params
        )
        return response.json()

    def add_spend_error(self, spend: dict) -> ErrorResponseModel:
        response = self.session.post(
            "/api/spends/add",
            json=spend,
            check_status=False
        )
        return ErrorResponseModel.model_validate(response.json())
