from requests import Response

from niffler_tests.utils.base_session import BaseSession


class CategoryApiClient:

    session: BaseSession

    def __init__(self, session: BaseSession) -> None:
        self.session = session

    def get_all_categories(self, exclude_archived: bool = False) -> Response:
        response = self.session.get(
            "/api/categories/all",
            params={"excludeArchived": exclude_archived}
        )
        response.raise_for_status()
        return response

    def add_category(self, category_name: str) -> Response:
        payload = {"name": category_name}
        return self.session.post(
            "/api/categories/add",
            json=payload
        )

    def update_category(self, category_id: str, category_name: str, archived: bool) -> Response:
        payload = {
            "id": category_id,
            "name": category_name,
            "archived": archived
        }
        return self.session.patch(
            "/api/categories/update",
            json=payload
        )
