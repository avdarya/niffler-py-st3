from niffler_tests_python.model.rest_model.category import CategoryModel
from niffler_tests_python.model.rest_model.error_response import ErrorResponseModel
from niffler_tests_python.utils.sessions import BaseSession


class CategoryApiClient:

    session: BaseSession

    def __init__(self, session: BaseSession) -> None:
        self.session = session

    def get_all_categories(self, exclude_archived: bool = False) -> list[CategoryModel]:
        response = self.session.get(
            "/api/categories/all",
            params={"excludeArchived": exclude_archived}
        )
        return [CategoryModel.model_validate(item) for item in response.json()]

    def add_category(self, category_name: str) -> CategoryModel:
        payload = {"name": category_name}
        response = self.session.post(
            "/api/categories/add",
            json=payload
        )
        return CategoryModel.model_validate(response.json())

    def update_category(self, category: CategoryModel) -> CategoryModel:
        response = self.session.patch(
            "/api/categories/update",
            json=category.model_dump()
        )
        return CategoryModel.model_validate(response.json())

    def add_category_error(self, category: dict) -> ErrorResponseModel:
        response = self.session.post(
            "/api/categories/add",
            json=category,
            check_status=False
        )
        return ErrorResponseModel.model_validate(response.json())

    def update_category_error(self, category: dict) -> ErrorResponseModel:
        response = self.session.patch(
            "/api/categories/update",
            json=category,
            check_status=False
        )
        return ErrorResponseModel.model_validate(response.json())


