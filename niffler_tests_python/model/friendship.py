from datetime import datetime
from sqlmodel import Field

from niffler_tests_python.model._bases import UserdataDBBase
from niffler_tests_python.model.enums.friendship_status import FriendshipDBStatus


class FriendshipModelDB(UserdataDBBase, table=True):
    __tablename__ = 'friendship'

    requester_id: str = Field(primary_key=True)
    addressee_id: str = Field(primary_key=True)
    status: FriendshipDBStatus
    created_date: datetime