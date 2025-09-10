import json
from typing import List

import pytest
from allure import step, epic, suite, title, id, tag
from faker import Faker

from niffler_tests_python.clients.kafka_client import KafkaClient
from niffler_tests_python.clients.oauth_client import OAuthClient
from niffler_tests_python.databases.userdata_db import UserdataDB
from niffler_tests_python.model.userdata import UserdataModelDB, UserName
from niffler_tests_python.utils.waiters import wait_until_timeout


@epic('[KAFKA][niffler-auth]: Паблишинг сообщений в кафку')
@suite('[KAFKA][niffler-auth]: Паблишинг сообщений в кафку')
class TestAuthRegistrationKafkaTest:
    @id('600001')
    @title("KAFKA: Сообщение с пользователем публикуется в Kafka после успешной регистрации")
    @tag("KAFKA")
    def test_message_should_be_produced_to_kafka_after_successful_registration(
            self,
            auth_client: OAuthClient,
            kafka: KafkaClient,
            userdata_db: UserdataDB
    ):
        username = Faker().user_name()
        password = Faker().password(special_chars=False)

        topic_partitions = kafka.subscribe_listen_new_offsets('users')

        result = auth_client.register(username, password)
        assert result.status_code == 201

        event = kafka.log_msg_and_json(topic_partitions)

        with step('Check that message from kafka exist'):
            assert event != '' and event != b''

        with step("Check message content"):
            data = json.loads(event.decode('utf8'))
            UserName.model_validate(data)
            assert data['username'] == username

    @id('600002')
    @title("KAFKA: После отправки в Kafka сообщения с пользователем в БД создается запись с пользователем")
    @tag("KAFKA")
    def test_user_registration_message_should_be_consumed_by_kafka(
            self,
            auth_client: OAuthClient,
            kafka: KafkaClient,
            userdata_db: UserdataDB
    ):
        username = Faker().user_name()

        kafka.produce_message('users', {'username': username})

        user_from_db = wait_until_timeout(userdata_db.get_userdata_by_username)(username)

        with step("Check that username from DB matches produced Kafka message"):
            assert user_from_db.username == username
        with step("Check setting default_currency for user"):
            assert user_from_db.currency == 'RUB'

    @id('600003')
    @title("KAFKA: После отправки в Kafka n сообщений с пользователями в БД создается n записей с пользователями")
    @tag("KAFKA")
    @pytest.mark.parametrize('user_count', [10])
    def test_multiple_registration_messages_should_be_consumed_by_kafka(
            self,
            user_count: int,
            auth_client: OAuthClient,
            kafka: KafkaClient,
            userdata_db: UserdataDB
    ):
        all_users_db: List[UserdataModelDB] = []
        added_username: List[str] = []
        for _ in range(user_count):
            username = Faker().user_name()
            added_username.append(username)
            kafka.produce_message('users', {'username': username})
            user_from_db = wait_until_timeout(userdata_db.get_userdata_by_username)(username)
            all_users_db.append(user_from_db)

        with step("Check that number of records in DB equals number of produced Kafka message"):
            assert len(all_users_db) == user_count

        with step("Check usernames in DB equal added usernames"):
            assert [user.username for user in all_users_db] == added_username

    @id('600004')
    @title("KAFKA: После отправки в Kafka сообщения с повторным пользователем в БД не создается дублирующая запись")
    @tag("KAFKA")
    def test_send_to_kafka_duplicate_user_registration_message(
            self,
            auth_client: OAuthClient,
            kafka: KafkaClient,
            userdata_db: UserdataDB
    ):
        username = Faker().user_name()
        kafka.produce_message('users', {'username': username})
        wait_until_timeout(userdata_db.get_userdata_by_username)(username)

        kafka.produce_message('users', {'username': username})
        user_from_db = userdata_db.get_all_records_by_username(username)

        with step("Check that duplicate Kafka message does not create duplicate user record in DB"):
            assert len(user_from_db) == 1
            assert user_from_db[0].username == username
