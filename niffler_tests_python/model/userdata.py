from typing import Optional
from pydantic import BaseModel
from sqlmodel import Field

from niffler_tests_python.model._bases import UserdataDBBase
from niffler_tests_python.model.enums.friendship_status import FriendshipAPIStatus


class UserModel(BaseModel):
    id: str
    username: str
    fullname: str
    currency: str

class UserName(BaseModel):
    username: str

class UserModelUpdate(BaseModel):
    id: str | None
    username: str | None
    fullname: str | None
    photo: str | None

class UserFriendshipModel(BaseModel):
    id: str
    username: str
    currency: str
    friendshipStatus: FriendshipAPIStatus | None = None
    fullname: str | None = None

class UserModelDB(UserdataDBBase, table=True):
    __tablename__ = "user"

    id: str = Field(default=None, primary_key=True)
    username: str
    currency: str
    firstname: Optional[str]
    surname: Optional[str]
    photo: Optional[bytes]
    photo_small: Optional[bytes]
    full_name: Optional[str]
