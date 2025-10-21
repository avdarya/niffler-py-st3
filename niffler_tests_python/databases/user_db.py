from typing import Sequence

from sqlmodel import select
from sqlalchemy import func


from niffler_tests_python.databases.userdata_base_db import UserdataBaseDB
from niffler_tests_python.model.userdata import UserModelDB
from niffler_tests_python.settings.server_config import ServerConfig


class UserDB(UserdataBaseDB):

    def __init__(self, server_config: ServerConfig):
        super().__init__(server_config)

    def get_userdata_by_username(self, username: str) -> UserModelDB:
        statement = select(UserModelDB).where(UserModelDB.username == username)
        return self.execute(self.engine, statement, 'one_or_none')

    def get_all_records_by_username(self, username: str) -> Sequence[UserModelDB]:
        statement = select(UserModelDB).where(UserModelDB.username == username)
        return self.execute(self.engine, statement, 'all')

    def delete_user(self, username: str) -> None:
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