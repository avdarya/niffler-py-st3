from typing import Sequence

import allure
from sqlalchemy import delete
from sqlalchemy.engine import ScalarResult
from sqlmodel import Session, select
from sqlalchemy import Engine, create_engine, event, text

from niffler_tests_python.model.auth_user_db import AuthUserModelDB
from niffler_tests_python.model.authority_db import AuthorityModelDB
from niffler_tests_python.settings.server_config import ServerConfig
from niffler_tests_python.utils.allure_helpers import attach_sql


class AuthDB:

    engine: Engine

    def __init__(self, server_config: ServerConfig):
        self.engine = create_engine(f'{server_config.auth_db_url}')
        event.listen(self.engine, 'do_execute', fn=attach_sql)

    @allure.step('[DB] Get user record by username')
    def get_by_username(self, username: str) -> AuthUserModelDB:
        with Session(self.engine) as session:
            statement = select(AuthUserModelDB).where(AuthUserModelDB.username == username)
            result: ScalarResult[AuthUserModelDB] = session.exec(statement)
            return result.one_or_none()

    @allure.step('[DB] Get all userdata records by username')
    def get_all_records_by_username(self, username: str) -> Sequence[AuthUserModelDB]:
        with Session(self.engine) as session:
            statement = select(AuthUserModelDB).where(AuthUserModelDB.username == username)
            result: ScalarResult[AuthUserModelDB] = session.exec(statement)
            return result.all()

    @allure.step('[DB] Delete user record by username')
    def delete_by_username(self, username: str) -> None:
        with Session(self.engine) as session:
            statement = select(AuthUserModelDB).where(AuthUserModelDB.username == username)
            users = session.exec(statement).all()
            for user in users:
                session.exec(delete(AuthorityModelDB).where(AuthorityModelDB.user_id == user.id))
                session.delete(user)
            session.commit()