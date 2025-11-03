import allure
import pytest
from niffler_tests_python.utils.marks import Pages
from niffler_tests_python.web_pages.components.HeaderComponent import HeaderComponent
from niffler_tests_python.web_pages.MainPage import MainPage
from niffler_tests_python.web_pages.ProfilePage import ProfilePage


@allure.epic("Траты")
@allure.feature("Создание категории")
@allure.story("UI")
@allure.tag("negative")
@allure.title("Добавление пустой категории")
@Pages.go_to_profile_page
def test_add_empty_category(profile_page: ProfilePage):
    with allure.step("Нажимаем на кнопку добавления категории и отправляем пустое значение"):
        profile_page.click_add_category()
        profile_page.submit_add_category()

    with allure.step("Проверяем появление текста-подсказки о некорректном вводе"):
        profile_page.is_helper_text_add_category()

@allure.epic("Траты")
@allure.feature("Создание категории")
@allure.story("UI")
@allure.tag("negative")
@allure.title("Добавление категории с недопустимой длиной названия")
@Pages.go_to_profile_page
@pytest.mark.parametrize("category_name", ["1"])
def test_add_category_less_min_length(
        category_name: str,
        main_page: MainPage,
        header: HeaderComponent,
        profile_page: ProfilePage,
):
    with allure.step("Вводим некорректное значение категории и отправляем форму"):
        profile_page.enter_add_category(category_name)
        profile_page.submit_add_category()

    with allure.step("Проверяем появление текста-подсказки о некорректном вводе"):
        profile_page.is_helper_text_add_category()
