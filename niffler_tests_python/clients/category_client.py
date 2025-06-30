from niffler_tests_python.model.category import CategoryModel
from niffler_tests_python.utils.base_session import BaseSession


class CategoryApiClient:

    session: BaseSession

    def __init__(self, session: BaseSession) -> None:
        self.session = session

    def get_all_categories(self, exclude_archived: bool = False) -> list[CategoryModel]:
        response = self.session.get(
            "/api/categories/all",
            params={"excludeArchived": exclude_archived}
        )
        response.raise_for_status()
        return [CategoryModel.model_validate(item) for item in response.json()]

    def add_category(self, category_name: str) -> CategoryModel:
        payload = {"name": category_name}
        response = self.session.post(
            "/api/categories/add",
            json=payload
        )
        response.raise_for_status()
        return CategoryModel.model_validate(response.json())

    def update_category(self, category: CategoryModel) -> CategoryModel:
        response = self.session.patch(
            "/api/categories/update",
            json=category.model_dump()
        )
        response.raise_for_status()
        return CategoryModel.model_validate(response.json())
