import pytest
from niffler_tests.clients.user_client import UserApiClient
from niffler_tests.web_pages.HeaderPage import HeaderPage
from niffler_tests.web_pages.MainPage import MainPage
from niffler_tests.web_pages.ProfilePage import ProfilePage

@pytest.mark.parametrize("name", ["Alex"])
def test_update_name(
        go_to_profile_page: None,
        profile_page: ProfilePage,
        user_client: UserApiClient,
        name: str
):
    profile_page.enter_name(name)
    profile_page.click_save_changes()

    alert_text = profile_page.alert_on_action()

    api_user = user_client.get_current_user()
    assert api_user.status_code == 200
    body = api_user.json()

    assert "Profile successfully updated" in alert_text
    assert name == body["fullname"]
