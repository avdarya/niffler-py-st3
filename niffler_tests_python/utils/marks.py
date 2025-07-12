import pytest
from _pytest.mark import MarkDecorator

from niffler_tests_python.model.spend import SpendModelAdd


class Pages:
    go_to_main_page = pytest.mark.usefixtures("go_to_main_page")
    go_to_main_page_after_spend = pytest.mark.usefixtures("go_to_main_page_after_spend")
    go_to_main_page_after_fill_spends = pytest.mark.usefixtures("go_to_main_page_after_fill_spends")
    go_to_profile_page = pytest.mark.usefixtures("go_to_profile_page")
    go_to_profile_after_category = pytest.mark.usefixtures("go_to_profile_after_category")


class TestData:
    fill_spends = pytest.mark.usefixtures("fill_spends")
    fill_categories = pytest.mark.usefixtures("fill_categories")

    @staticmethod
    def category(x: str) -> MarkDecorator:
        return pytest.mark.parametrize("category", [x], indirect=True)

    @staticmethod
    def two_categories(x: tuple[str, str]) -> MarkDecorator:
        return pytest.mark.parametrize(
            "two_categories",
            [x],
            indirect=True,
            ids="two_categories"
    )

    @staticmethod
    def archive_category(x: str) -> MarkDecorator:
        return pytest.mark.parametrize("archive_category", [x], indirect=True)

    @staticmethod
    def spend(x: SpendModelAdd) -> MarkDecorator:
        return pytest.mark.parametrize(
            "spend",
            [x],
            indirect=True,
            ids=lambda param: param.description
        )

    @staticmethod
    def custom_date_spend(x: SpendModelAdd) -> MarkDecorator:
        return pytest.mark.parametrize(
        "custom_date_spend",
        [x],
        indirect=True,
        ids=lambda param: param.description
    )
