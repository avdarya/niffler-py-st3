import pytest
from _pytest.mark import MarkDecorator

from niffler_tests_python.model.rest_model.spend import SpendModelAdd


class Pages:
    go_to_main_page = pytest.mark.usefixtures("go_to_main_page")
    go_to_main_page_after_spend = pytest.mark.usefixtures("go_to_main_page_after_spend")
    go_to_main_page_after_fill_spends = pytest.mark.usefixtures("go_to_main_page_after_fill_spends")
    go_to_profile_page = pytest.mark.usefixtures("go_to_profile_page")
    go_to_profile_after_category = pytest.mark.usefixtures("go_to_profile_after_category")
    go_to_people_all_after_people = pytest.mark.usefixtures("go_to_people_all_after_people")
    go_to_people_friends_after_send = pytest.mark.usefixtures("go_to_people_friends_after_send")
    go_to_people_friends_after_accept = pytest.mark.usefixtures("go_to_people_friends_after_accept")
    go_to_people_all_after_list_people = pytest.mark.usefixtures("go_to_people_all_after_list_people")
    go_to_people_friends_after_list_friend = pytest.mark.usefixtures("go_to_people_friends_after_list_friend")

class TestData:
    fill_spends = pytest.mark.usefixtures("fill_spends")
    fill_categories = pytest.mark.usefixtures("fill_categories")
    filled_spends_contains_archived_category = pytest.mark.usefixtures("filled_spends_contains_archived_category")

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

    @staticmethod
    def people_list(x: int) -> MarkDecorator:
        return pytest.mark.parametrize("people_list", [x], indirect=True)

    @staticmethod
    def friend_list(x: int) -> MarkDecorator:
        return pytest.mark.parametrize("friend_list", [x], indirect=True)
