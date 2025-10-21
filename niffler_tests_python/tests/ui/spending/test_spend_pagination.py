import allure
from niffler_tests_python.clients.spend_client import SpendApiClient
from niffler_tests_python.utils.marks import Pages, TestData
from niffler_tests_python.web_pages.MainPage import MainPage


@allure.epic("Траты")
@allure.feature("Пагинация трат")
@allure.story("UI")
@allure.tag("positive")
@allure.title("Переход на следующую страницу трат")
@Pages.go_to_main_page_after_fill_spends
@TestData.fill_spends
def test_next_page(main_page: MainPage, spend_client: SpendApiClient):
    with allure.step('Переходим на следующую страницу'):
        main_page.click_next_button()

    with allure.step('Получаем данные трат для следующей страницы через API'):
        api_next_page = spend_client.get_all_spends_v2(page=1)
        api_spend_ids = [spend_item["id"] for spend_item in api_next_page["content"]]

    with allure.step('Сохраняем идентификаторы трат следующей страницы из UI'):
        ui_spend_ids = main_page.get_spend_ids()

    with allure.step('Проверяем корректность данных следующей страницы'):
        with allure.step('Количество трат на следующей странице в API совпадает с количеством в UI'):
            assert len(api_next_page["content"]) == len(ui_spend_ids)
    with allure.step('Идентификаторы трат следующей страницы в API совпадают с UI'):
        assert api_spend_ids == ui_spend_ids

@allure.epic("Траты")
@allure.feature("Пагинация трат")
@allure.story("UI")
@allure.tag("positive")
@allure.title("Переход на предыдущую страницу трат")
@Pages.go_to_main_page_after_fill_spends
@TestData.fill_spends
def test_previous_page(main_page: MainPage, spend_client: SpendApiClient):
    with allure.step('Переходим на следующую страницу'):
        main_page.click_next_button()

    with allure.step('Переходим на предыдущую страницу'):
        main_page.click_previous_button()

    with allure.step('Получаем данные трат для предыдущей страницы через API'):
        api_previous_page = spend_client.get_all_spends_v2()
        api_spend_ids = [spend_item["id"] for spend_item in api_previous_page["content"]]

    with allure.step('Сохраняем идентификаторы трат предыдущей страницы из UI'):
        ui_spend_ids = main_page.get_spend_ids()

    with allure.step('Проверяем корректность данных предыдущей страницы'):
        with allure.step('Количество трат на предыдущей странице в API совпадает с количеством в UI'):
            assert len(api_previous_page["content"]) == len(ui_spend_ids)
        with allure.step('Идентификаторы трат предыдущей страницы в API совпадают с UI'):
            assert api_spend_ids == ui_spend_ids
