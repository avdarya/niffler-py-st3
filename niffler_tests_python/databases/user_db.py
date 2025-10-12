from typing import Sequence

import allure
from sqlalchemy import Engine, create_engine, event, ScalarResult
from sqlmodel import Session, select
from sqlalchemy import func


from niffler_tests_python.databases.userdata_base_db import UserdataBaseDB
from niffler_tests_python.model.userdata import UserModelDB
from niffler_tests_python.settings.server_config import ServerConfig
from niffler_tests_python.utils.allure_helpers import attach_sql


class UserDB(UserdataBaseDB):

    def __init__(self, server_config: ServerConfig):
        super().__init__(server_config)
        # self.engine = create_engine(f'{server_config.userdata_db_url}')
        # event.listen(self.engine, 'do_execute', fn=attach_sql)

    @allure.step('[DB] Get userdata record by username')
    def get_userdata_by_username(self, username: str) -> UserModelDB:
        # with Session(self.engine) as session:
        #     statement = select(UserdataModelDB).where(UserdataModelDB.username == username)
        #     result: ScalarResult[UserdataModelDB] = session.exec(statement)
        #     return result.one_or_none()
        statement = select(UserModelDB).where(UserModelDB.username == username)
        return self.execute(self.engine, statement, 'one_or_none')

    @allure.step('[DB] Get all userdata records by username')
    def get_all_records_by_username(self, username: str) -> Sequence[UserModelDB]:
        # with Session(self.engine) as session:
        #     statement = select(UserdataModelDB).where(UserdataModelDB.username == username)
        #     result: ScalarResult[UserdataModelDB] = session.exec(statement)
        #     return result.all()
        statement = select(UserModelDB).where(UserModelDB.username == username)
        return self.execute(self.engine, statement, 'all')

    @allure.step('[DB] Delete userdata record')
    def delete_user(self, username: str) -> None:
        # with Session(self.engine) as session:
        #     statement = select(UserModelDB).where(UserModelDB.username == username)
        #     result: ScalarResult[UserModelDB] = session.exec(statement)
        #     users = result.all()
        #     for user in users:
        #         session.delete(user)
        #     session.commit()
        self.delete_records(self.engine, UserModelDB, UserModelDB.username == username)

    def get_users_by_filter(
            self,
            page: int,
            size: int,
            sort: str,
            direction: str = 'ASC',
            search_query: str = '',
    ) -> list[UserModelDB]:
        statement = select(UserModelDB)

        if search_query:
            statement = statement.where(UserModelDB.username.ilike(f'%{search_query}%'))

        if direction == 'ASC':
            statement = statement.order_by(getattr(UserModelDB, sort).asc())
        else:
            statement = statement.order_by(getattr(UserModelDB, sort).desc())

        statement = statement.limit(size).offset(page*size)

        return self.execute(self.engine, statement, 'all')

    def get_users_count(self, search_query: str = '') -> int:
        statement = select(func.count()).select_from(UserModelDB)

        if search_query:
            statement = statement.where(UserModelDB.username.ilike(f'%{search_query}%'))

        return self.execute(self.engine, statement, 'scalar').one()