import pytest
from niffler_tests_python.clients.user_client import UserApiClient
from niffler_tests_python.databases.userdata_db import UserdataDB
from niffler_tests_python.tests.conftest import Pages
from niffler_tests_python.web_pages.ProfilePage import ProfilePage


@Pages.go_to_profile_page
@pytest.mark.parametrize("fullname", ["Alex", "Mike"])
def test_update_name(
        profile_page: ProfilePage,
        user_client: UserApiClient,
        userdata_db: UserdataDB,
        fullname
):
    profile_page.clear_name_input()
    profile_page.enter_name(fullname)
    profile_page.click_save_changes()
    alert_text = profile_page.alert_on_action()

    api_user = user_client.get_current_user()

    db_userdata = userdata_db.get_userdata_by_username(api_user.username)

    assert "Profile successfully updated" in alert_text
    assert fullname == api_user.fullname
    assert db_userdata.full_name == fullname
