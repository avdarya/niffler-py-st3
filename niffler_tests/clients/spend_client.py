from requests import Response

from niffler_tests.utils.base_session import BaseSession


class SpendApiClient:

    session: BaseSession

    def __init__(self, session: BaseSession):
        self.session = session

    def get_all_spends(self, filter_currency: str = None, filter_period: str = None) -> Response:
        return self.session.get(
            "/api/spends/all",
            params={"filterCurrency": filter_currency, "filterPeriod": filter_period}
        )

    def add_spending(self, spend: dict) -> Response:
        return self.session.post(
            "/api/spends/add",
            json=spend
        )

    def delete_spending(self, ids: list[str]) -> Response:
        return self.session.delete(
            "/api/spends/remove",
            params={"ids": ",".join(ids)}
        )

    def get_all_spends_v2(
            self,
            page: int = 0,
            search_query: str = None,
            filter_period: str = None,
            filter_currency: str = None
    ) -> Response:
        params = {
            "page": page,
            "searchQuery": search_query,
            "filterPeriod": filter_period,
            "filterCurrency": filter_currency
        }
        return self.session.get(
            "/api/v2/spends/all",
            params=params
        )
