import allure
import pytest
from niffler_tests_python.clients.user_client import UserApiClient
from niffler_tests_python.databases.userdata_db import UserdataDB
from niffler_tests_python.utils.marks import Pages
from niffler_tests_python.web_pages.ProfilePage import ProfilePage


@allure.epic('Userdata management')
@allure.feature('Userdata updating')
@allure.story('Update fullname')
@Pages.go_to_profile_page
@pytest.mark.parametrize("fullname", ["Alex", "Mike"])
def  test_update_name(
        profile_page: ProfilePage,
        user_client: UserApiClient,
        userdata_db: UserdataDB,
        fullname
):
    with allure.step('Enter fullname'):
        profile_page.clear_name_input()
        profile_page.enter_name(fullname)

    with allure.step('Click save changes button'):
        profile_page.click_save_changes()

    with allure.step('Save alert dialog'):
        alert_text = profile_page.alert_on_action()

    with allure.step('Retrieve userdata from API'):
        api_user = user_client.get_current_user()

    with allure.step('Retrieve userdata from DB'):
        db_userdata = userdata_db.get_userdata_by_username(api_user.username)

    with allure.step('Assert update name'):
        with allure.step('Verify alert text'):
            assert "Profile successfully updated" in alert_text
        with allure.step('Verify fullname in API'):
            assert fullname == api_user.fullname
        with allure.step('Verify fullname in DB'):
            assert db_userdata.full_name == fullname
