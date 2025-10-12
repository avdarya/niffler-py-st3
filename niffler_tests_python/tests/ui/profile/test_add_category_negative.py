import allure
import pytest
from niffler_tests_python.utils.marks import Pages
from niffler_tests_python.web_pages.components.HeaderComponent import HeaderComponent
from niffler_tests_python.web_pages.MainPage import MainPage
from niffler_tests_python.web_pages.ProfilePage import ProfilePage


@allure.epic('Spending management')
@allure.feature('Category creation')
@allure.story('Add empty category')
@Pages.go_to_profile_page
def test_add_empty_category(profile_page: ProfilePage):
   with allure.step('Click and submit empty new category input'):
      profile_page.click_add_category()
      profile_page.submit_add_category()
   with allure.step('Verify helper text for category input'):
      profile_page.is_helper_text_add_category()

@allure.epic('Spending management')
@allure.feature('Category creation')
@allure.story('Add category with invalid value')
@Pages.go_to_profile_page
@pytest.mark.parametrize("category_name", ["1"])
def test_add_category_less_min_length(
        category_name: str,
        main_page: MainPage,
        header: HeaderComponent,
        profile_page: ProfilePage,
):
   with allure.step('Fill and submit new category with invalid value'):
      profile_page.enter_add_category(category_name)
      profile_page.submit_add_category()

   with allure.step('Verify helper text for category input'):
      profile_page.is_helper_text_add_category()
