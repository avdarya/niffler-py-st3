from typing import Optional
from sqlmodel import select
from sqlalchemy import func, distinct
from niffler_tests_python.databases.userdata_base_db import UserdataBaseDB
from niffler_tests_python.model.enums.friendship_status import FriendshipDBStatus
from niffler_tests_python.model.db_model.friendship_db import FriendshipModelDB
from niffler_tests_python.model.db_model.userdata_db import UserModelDB
from niffler_tests_python.settings.server_config import ServerConfig


class FriendshipDB(UserdataBaseDB):

    def __init__(self, server_config: ServerConfig):
        super().__init__(server_config)

    def get_friendship(self, requester_id: str, addressee_id: str) -> Optional[FriendshipModelDB]:
        statement = (select(FriendshipModelDB)
            .where(FriendshipModelDB.requester_id == requester_id)
            .where(FriendshipModelDB.addressee_id == addressee_id))
        return self.execute(self.engine, statement, 'one_or_none')

    def delete_by_requester_id(self, requested_id: str) -> None:
        self.delete_records(
            self.engine,
            FriendshipModelDB,
            FriendshipModelDB.requester_id == requested_id
        )

    def delete_by_addressee_id(self, addressee_id: str) -> None:
        self.delete_records(
            self.engine,
            FriendshipModelDB,
            FriendshipModelDB.addressee_id == addressee_id
        )

    def get_friends_by_filter(
            self,
            user_id: str,
            page: int,
            size: int,
            sort: str,
            direction: str = 'ASC',
            search_query: str = '',
    ) -> list[UserModelDB]:
        f = FriendshipModelDB
        u = UserModelDB
        statement = (
            select(u).distinct()
            .join(
                f,
                ((f.addressee_id == u.id) & (f.requester_id == user_id))
                | ((f.requester_id == u.id) & (f.addressee_id == user_id))
            )
            .where(f.status == FriendshipDBStatus.ACCEPTED)
            .where(u.id != user_id)
        )

        if search_query:
            statement = statement.where(u.username.ilike(f'%{search_query}%'))

        if direction == 'ASC':
            statement = statement.order_by(getattr(u, sort).asc())
        else:
            statement = statement.order_by(getattr(u, sort).desc())

        statement = statement.limit(size).offset(page * size)

        return self.execute(self.engine, statement, 'all')

    def get_friends_count(
        self,
        user_id: str,
        search_query: str = '',
    ) -> int:
        f = FriendshipModelDB
        u = UserModelDB

        statement = (
            select(func.count(distinct(u.id)))
            .select_from(u)
            .join(
                f,
                ((f.addressee_id == u.id) & (f.requester_id == user_id))
                | ((f.requester_id == u.id) & (f.addressee_id == user_id))
            )
            .where(f.status == FriendshipDBStatus.ACCEPTED)
            .where(u.id != user_id)
        )

        if search_query:
            statement = statement.where(u.username.ilike(f'%{search_query}%'))

        return self.execute(self.engine, statement, 'scalar').one()