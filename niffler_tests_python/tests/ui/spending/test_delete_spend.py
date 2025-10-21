import allure
from niffler_tests_python.clients.spend_client import SpendApiClient
from niffler_tests_python.databases.spend_db import SpendDB
from niffler_tests_python.model.spend import SpendModelAdd, SpendModel
from niffler_tests_python.utils.helpers import wait_for_spend_row
from niffler_tests_python.utils.marks import Pages, TestData
from niffler_tests_python.web_pages.MainPage import MainPage


@allure.epic("Траты")
@allure.feature("Удаление трат")
@allure.story("UI")
@allure.tag("positive")
@allure.title("Удаление одной траты через интерфейс")
@Pages.go_to_main_page_after_spend
@TestData.spend(SpendModelAdd(
    amount=9.01,
    description="test delete spending by one",
    currency="EUR",
    spendDate="2025-06-23T21:00:00.000+00:00",
    category={"name": "spend delete by one"}
))
def test_delete_spending_by_one(
        main_page: MainPage,
        spend: SpendModel,
        spend_client: SpendApiClient,
        spend_db: SpendDB
):
    with allure.step('Получаем количество трат до удаления'):
        before_spending = spend_client.get_all_spends()
        before_spending_count = len(before_spending)

    with allure.step('Находим трату для удаления'):
        spend_row = wait_for_spend_row(main_page, spend.id)
        assert spend_row is not None

    with allure.step('Выбираем строку траты'):
        main_page.click_checkbox(spend_row)
    with allure.step('Проверяем состояние чекбокса после выбора'):
        main_page.checkbox_should_checked(spend_row)

    with allure.step('Удаляем выбранную трату'):
        main_page.click_delete_button()
        main_page.click_popup_delete_button()

    with allure.step('Проверяем уведомление об успешном удалении'):
        main_page.notification.is_info_notification()
        assert "Spendings succesfully deleted" == main_page.notification.get_notification_text()

    with allure.step('Проверяем отсутствие удалённой траты в таблице'):
        spend_row_after_deleted = main_page.get_spend_row_by_id(spend_id=spend.id)

    with allure.step('Получаем количество трат после удаления'):
        after_spending = spend_client.get_all_spends()
        after_spending_count = len(after_spending)

    with allure.step('Проверяем отсутствие удалённой траты в БД'):
        db_spend = spend_db.get_spend(spend.id)

    with allure.step('Проверяем корректность удаления траты'):
        with allure.step('Количество трат после = количество до - 1'):
            assert before_spending_count - 1 == after_spending_count
        with allure.step('Удалённая трата отсутствует в UI'):
            assert spend_row_after_deleted is None
        with allure.step('Удалённая запись отсутствует в БД'):
            assert db_spend is None

@allure.epic("Траты")
@allure.feature("Удаление трат")
@allure.story("UI")
@allure.tag("positive")
@allure.title("Удаление списка трат через интерфейс")
@Pages.go_to_main_page_after_fill_spends
@TestData.fill_spends
def test_delete_spending_by_list(main_page: MainPage, spend_client: SpendApiClient, spend_db: SpendDB):
    with allure.step('Получаем количество трат до удаления'):
        before_spending = spend_client.get_all_spends()
        before_spending_count = len(before_spending)

    with allure.step('Выбираем все строки трат через чекбокс в заголовке таблицы'):
        main_page.select_all_rows()
        selected_spend_ids = main_page.get_selected_spend_ids()

    with allure.step('Удаляем выбранные траты'):
        main_page.click_delete_button()
        main_page.click_popup_delete_button()

    with allure.step('Проверяем уведомление об успешном удалении'):
        main_page.notification.is_info_notification()
        assert "Spendings succesfully deleted" == main_page.notification.get_notification_text()

    with allure.step('Сохраняем id трат, отображаемых после удаления'):
        ui_spend_ids_after_deleted = main_page.get_spend_ids()

    with allure.step('Получаем количество трат и id после удаления'):
        after_spending = spend_client.get_all_spends()
        after_spending_count = len(after_spending)
        after_spend_ids = [spend.id for spend in after_spending]

    with allure.step('Проверяем отсутствие удалённых трат в БД'):
        assert len(spend_db.get_spend_list(selected_spend_ids)) == 0

    with allure.step('Проверяем корректность удаления трат после мультивыбора'):
        with allure.step('Количество трат после = количество до - количество выбранных'):
            assert before_spending_count - len(selected_spend_ids) == after_spending_count

        with allure.step('Проверяем, что удалённые траты отсутствуют в API'):
            assert set(after_spend_ids).isdisjoint(selected_spend_ids)
        with allure.step('Проверяем, что удалённые траты отсутствуют в UI'):
            assert set(ui_spend_ids_after_deleted).isdisjoint(selected_spend_ids)

@allure.epic("Траты")
@allure.feature("Удаление трат")
@allure.story("UI")
@allure.tag("positive")
@allure.title("Отмена удаления траты через интерфейс")
@Pages.go_to_main_page_after_spend
@TestData.spend(SpendModelAdd(
    amount=12.01,
    description="test cancel delete spend",
    currency="USD",
    spendDate="2025-06-26T21:00:00.000+00:00",
    category={"name": "cancel delete spend"}
))
def test_cancel_delete_spend(
        main_page: MainPage,
        spend: SpendModel,
        spend_client: SpendApiClient,
        spend_db: SpendDB
):
    with allure.step('Получаем количество трат до удаления'):
        before_spending = spend_client.get_all_spends()
        before_spending_count = len(before_spending)

    with allure.step('Находим трату для удаления'):
        spend_row = wait_for_spend_row(main_page, spend.id)
        assert spend_row is not None

    with allure.step('Выбираем строку траты для удаления'):
        main_page.click_checkbox(spend_row)

    with allure.step('Нажимаем кнопку удаления и отменяем удаление'):
        main_page.click_delete_button()
        main_page.click_popup_cancel_button()

    with allure.step('Снимаем выбор с чекбокса после отмены'):
        main_page.click_checkbox(spend_row)
    with allure.step('Проверяем состояние чекбокса после снятия выбора'):
        main_page.checkbox_should_unchecked(spend_row)

    with allure.step('Находим выбранную трату в таблице'):
        spend_row_after_deleted = main_page.get_spend_row_by_id(spend.id)

    with allure.step('Получаем количество трат после отмены удаления'):
        after_spending = spend_client.get_all_spends()
        after_spending_count = len(after_spending)

    with allure.step('Проверяем существование траты в БД'):
        db_spend = spend_db.get_spend(spend_id=spend.id)

    with allure.step('Проверяем, что трата осталась после отмены удаления'):
        with allure.step('Количество трат после = количество до'):
            assert before_spending_count == after_spending_count
        with allure.step('Проверяем, что выбранная строка есть в UI'):
            assert spend_row_after_deleted is not None
        with allure.step('Проверяем, что выбранная трата есть в БД'):
            assert db_spend is not None