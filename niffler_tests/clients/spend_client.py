import os

import dotenv
from requests import Response

from utils.base_session import BaseSession


class SpendApiClient:

    def __init__(self, session: BaseSession):
        self.session = session

    def get_token(self) -> str:
        dotenv.load_dotenv()
        token = os.getenv("TOKEN")
        return token

    def get_all_spends(self, filter_currency: str = None, filter_period: str = None) -> Response:
        headers = {'Authorization': f"Bearer {self.get_token()}"}
        return self.session.get(
            "/api/spends/all",
            params={"filterCurrency": filter_currency, "filterPeriod": filter_period},
            headers=headers
        )

    def add_spending(self, spend: dict) -> Response:
        headers = {'Authorization': f"Bearer {self.get_token()}"}
        return self.session.post(
            "/api/spends/add",
            json=spend,
            headers=headers
        )

    def delete_spending(self, ids: list[str]) -> Response:
        headers = {'Authorization': f"Bearer {self.get_token()}"}
        return self.session.delete(
            "/api/spends/remove",
            params={"ids": ",".join(ids)},
            headers=headers
        )