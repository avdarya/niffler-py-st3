from typing import Sequence

import allure
from sqlalchemy import Engine, create_engine, event
from sqlalchemy.engine import ScalarResult
from sqlmodel import Session, select

from niffler_tests_python.model.userdata import UserdataModelDB
from niffler_tests_python.settings.server_config import ServerConfig
from niffler_tests_python.utils.allure_helpers import attach_sql


class UserdataDB:

    engine: Engine

    def __init__(self, server_config: ServerConfig):
        self.engine = create_engine(f'{server_config.userdata_db_url}')
        event.listen(self.engine, 'do_execute', fn=attach_sql)

    @allure.step('[DB] Get userdata: username={username}')
    def get_userdata_by_username(self, username: str) -> UserdataModelDB:
        with Session(self.engine) as session:
            statement = select(UserdataModelDB).where(UserdataModelDB.username == username)
            result: ScalarResult[UserdataModelDB] = session.exec(statement)
            return result.one_or_none()

    @allure.step('[DB] Get userdata: username={username}')
    def get_all_records_by_username(self, username: str) -> Sequence[UserdataModelDB]:
        with Session(self.engine) as session:
            statement = select(UserdataModelDB).where(UserdataModelDB.username == username)
            result: ScalarResult[UserdataModelDB] = session.exec(statement)
            return result.all()
