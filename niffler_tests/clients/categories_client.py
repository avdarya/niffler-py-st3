import dotenv
import os

from requests import Response

from utils.base_session import BaseSession


class CategoriesApiClient:

    def __init__(self, session: BaseSession) -> None:
        self.session = session

    def get_token(self) -> str:
        dotenv.load_dotenv()
        token = os.getenv("TOKEN")
        return token

    def get_all_categories(self, excludeArchived: bool = False) -> Response:
        headers = {'Authorization': f"Bearer {self.get_token()}"}
        return self.session.get(
            "/api/categories/all",
            params={"excludeArchived": excludeArchived},
            headers=headers
        )

    def add_category(self, category_name: str) -> Response:
        payload = {"name": category_name}
        headers = {'Authorization': f"Bearer {self.get_token()}"}
        return self.session.post(
            "/api/categories/add",
            json=payload,
            headers=headers
        )

    def update_category(self, category_id: str, category_name: str, archived: bool) -> Response:
        payload = {
            "id": category_id,
            "name": category_name,
            "archived": archived
        }
        headers = {'Authorization': f"Bearer {self.get_token()}"}
        return self.session.patch(
            "/api/categories/update",
            json=payload,
            headers=headers
        )
