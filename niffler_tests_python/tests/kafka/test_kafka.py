import json
from typing import List

import pytest
import allure
from allure import step
from faker import Faker

from niffler_tests_python.clients.kafka_client import KafkaClient
from niffler_tests_python.clients.oauth_client import OAuthClient
from niffler_tests_python.databases.user_db import UserDB
from niffler_tests_python.model.rest_model.userdata import UserName
from niffler_tests_python.model.db_model.userdata_db import UserModelDB
from niffler_tests_python.utils.waiters import wait_until_timeout


@allure.epic("Авторизация")
@allure.feature("Регистрация")
@allure.story("Kafka")
@allure.tag("positive")
@allure.title("Сообщение о регистрации нового пользователя публикуется в Kafka после успешной регистрации")
@pytest.mark.isolated
def test_message_should_be_produced_to_kafka_after_successful_registration(
        auth_client: OAuthClient,
        kafka: KafkaClient,
        user_db: UserDB,
        fake: Faker,
        worker_id: str,
        cleanup_user
):
    username = f"{fake.user_name()}_{worker_id}"
    password = fake.password(special_chars=False)
    cleanup_user(username)

    topic_partitions = kafka.subscribe_listen_new_offsets('users')

    with step("Отправить запрос на регистрацию нового пользователя через API"):
        result = auth_client.register(username, password)
        assert result.status_code == 201, "Регистрация неуспешна"

    with step("Получить новое сообщение из Kafka"):
        event = kafka.log_msg_and_json(topic_partitions, worker_id)

    with step("Проверить, что сообщение из Kafka существует"):
        assert event not in ('', b'')

    with step("Проверить содержимое сообщения из Kafka"):
        data = json.loads(event.decode('utf8'))
        UserName.model_validate(data)
        assert data['username'] == username, "Имя пользователя в сообщении не совпадает с ожидаемым"

@allure.epic("Авторизация")
@allure.feature("Регистрация пользователя")
@allure.story("Kafka")
@allure.tag("positive")
@allure.title("После отправки сообщения с пользователем в Kafka запись создаётся в базе данных")
def test_user_registration_message_should_be_consumed_by_kafka(
        auth_client: OAuthClient,
        kafka: KafkaClient,
        user_db: UserDB,
        fake: Faker,
        worker_id: str,
        cleanup_user
):
    username = f"{fake.user_name()}_{worker_id}"
    cleanup_user(username)

    with step("Отправить сообщение о регистрации нового пользователя в Kafka"):
        kafka.produce_message('users', {'username': username})

    with step("Ожидать появления пользователя в базе данных"):
        user_from_db = wait_until_timeout(user_db.get_userdata_by_username)(username)

    with step("Проверить, что имя пользователя в базе совпадает с отправленным сообщением"):
        assert user_from_db.username == username, "Имя пользователя не совпадает"
    with step("Проверить, что пользователю установлена валюта по умолчанию"):
        assert user_from_db.currency == 'RUB', "Валюта по умолчанию не установлена"

@allure.epic("Авторизация")
@allure.feature("Регистрация пользователя")
@allure.story("Kafka")
@allure.tag("positive")
@allure.title("После отправки нескольких сообщений с пользователями в Kafka создаются соответствующие записи в базе данных")
@pytest.mark.parametrize('user_count', [10])
def test_multiple_registration_messages_should_be_consumed_by_kafka(
        user_count: int,
        auth_client: OAuthClient,
        kafka: KafkaClient,
        user_db: UserDB,
        fake: Faker,
        worker_id: str,
        cleanup_user
):
    all_users_db: List[UserModelDB] = []
    added_username: List[str] = []

    with step("Сформировать и отправить несколько сообщений с пользователями в Kafka"):
        for _ in range(user_count):
            username = f"{fake.user_name()}_{worker_id}"
            cleanup_user(username)
            added_username.append(username)
            kafka.produce_message('users', {'username': username})
            user_from_db = wait_until_timeout(user_db.get_userdata_by_username)(username)
            all_users_db.append(user_from_db)

    with step("Проверить, что количество пользователей в базе соответствует количеству сообщений"):
        assert len(all_users_db) == user_count, "Количество пользователей в базе не совпадает"

    with step("Проверить совпадение имён пользователей между Kafka и базой данных"):
        assert [user.username for user in all_users_db] == added_username, "Имена пользователей не совпадают"

@allure.epic("Авторизация")
@allure.feature("Регистрация пользователя")
@allure.story("Kafka")
@allure.tag("positive")
@allure.title("Повторная отправка сообщения с пользователем в Kafka не создаёт дубликат записи в базе данных")
def test_send_to_kafka_duplicate_user_registration_message(
        auth_client: OAuthClient,
        kafka: KafkaClient,
        user_db: UserDB,
        fake: Faker,
        worker_id: str,
        cleanup_user
):
    username = f"{fake.user_name()}_{worker_id}"
    cleanup_user(username)
    with step("Отправить сообщение о пользователе в Kafka и дождаться его появления в базе"):
        kafka.produce_message('users', {'username': username})
        wait_until_timeout(user_db.get_userdata_by_username)(username)

    with step("Повторно отправить сообщение о том же пользователе в Kafka"):
        kafka.produce_message('users', {'username': username})
        user_from_db = user_db.get_all_records_by_username(username)

    with step("Проверить, что в базе данных осталась только одна запись пользователя"):
        assert len(user_from_db) == 1, "Обнаружен дубликат пользователя в базе"
        assert user_from_db[0].username == username, "Имя пользователя не совпадает"
