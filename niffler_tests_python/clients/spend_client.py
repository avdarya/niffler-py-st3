from niffler_tests_python.model.spend import SpendModel, SpendModelAdd
from niffler_tests_python.utils.base_session import BaseSession


class SpendApiClient:

    session: BaseSession

    def __init__(self, session: BaseSession):
        self.session = session

    def get_all_spends(self, filter_currency: str = None, filter_period: str = None) -> list[SpendModel]:
        response = self.session.get(
            "/api/spends/all",
            params={"filterCurrency": filter_currency, "filterPeriod": filter_period}
        )
        response.raise_for_status()
        return [SpendModel.model_validate(item) for item in response.json()]

    def add_spend(self, spend: SpendModelAdd) -> SpendModel:
        response = self.session.post(
            "/api/spends/add",
            json=spend.model_dump()
        )
        response.raise_for_status()
        return SpendModel.model_validate(response.json())

    def delete_spend(self, ids: list[str]) -> None:
        response = self.session.delete(
            "/api/spends/remove",
            params={"ids": ",".join(ids)}
        )
        response.raise_for_status()

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
        response.raise_for_status()
        return response.json()
