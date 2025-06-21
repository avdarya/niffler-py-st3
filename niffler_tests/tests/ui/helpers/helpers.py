import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

from clients.categories_client import CategoriesApiClient


def login(driver: WebDriver, login_url: str, username: str, password: str) -> WebDriver:
    driver.get(f"{login_url}/login")

    driver.find_element(By.CSS_SELECTOR, 'input[name="username"]').send_keys(username)
    driver.find_element(By.CSS_SELECTOR, 'input[name="password"]').send_keys(password)

    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'img[alt="Niffler logo"]'))
    )

    return driver

def wait_for_category_update_name(
        categories_client: CategoriesApiClient,
        category_id: str,
        expected_name: str,
        timeout=5,
        interval=0.5
):
    end_time = time.time() + timeout
    while time.time() < end_time:
        resp = categories_client.get_all_categories()
        if resp.status_code != 200:
            continue

        categories = resp.json()
        for category in categories:
            if category["id"] == category_id and category["name"] == expected_name:
                return category
        time.sleep(interval)

    raise AssertionError(f"Категория {category_id} не обновилась на '{expected_name}' за {timeout} секунд")

def wait_for_category_update_archive(
        categories_client: CategoriesApiClient,
        category_id: str,
        expected_archive: bool,
        timeout=5,
        interval=0.5
):
    end_time = time.time() + timeout
    while time.time() < end_time:
        resp = categories_client.get_all_categories()
        if resp.status_code != 200:
            continue

        categories = resp.json()
        for category in categories:
            if category["id"] == category_id and category["archived"] == expected_archive:
                return category
        time.sleep(interval)

    raise AssertionError(f"Категория {category_id} не обновилась на '{expected_archive}' за {timeout} секунд")