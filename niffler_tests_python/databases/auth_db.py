from typing import Sequence

from sqlmodel import select
from sqlalchemy import Engine, create_engine, event

from niffler_tests_python.databases.base_db import BaseDB
from niffler_tests_python.model.db_model.auth_user_db import AuthUserModelDB
from niffler_tests_python.model.db_model.authority_db import AuthorityModelDB
from niffler_tests_python.settings.server_config import ServerConfig
from niffler_tests_python.utils.allure_helpers import attach_sql


class AuthDB(BaseDB):

    engine: Engine

    def __init__(self, server_config: ServerConfig):
        self.engine = create_engine(f'{server_config.auth_db_url}')
        event.listen(self.engine, 'do_execute', fn=attach_sql)

    def get_by_username(self, username: str) -> AuthUserModelDB:
        statement = select(AuthUserModelDB).where(AuthUserModelDB.username == username)
        return self.execute(self.engine, statement, 'one_or_none')

    def get_all_records_by_username(self, username: str) -> Sequence[AuthUserModelDB]:
        statement = select(AuthUserModelDB).where(AuthUserModelDB.username == username)
        return self.execute(self.engine, statement, 'all')

    def delete_by_username(self, username: str) -> None:
        users = self.execute(
            self.engine,
            select(AuthUserModelDB).where(AuthUserModelDB.username == username),
            fetch='all'
        )
        for user in users:
            self.delete_records(self.engine, AuthorityModelDB, AuthorityModelDB.user_id == user.id)
        self.delete_records(self.engine, AuthUserModelDB, AuthUserModelDB.username == username)
