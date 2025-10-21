from typing import Optional
from pydantic import BaseModel
from sqlmodel import Field

from niffler_tests_python.model._bases import UserdataDBBase
from niffler_tests_python.model.category import CategoryGqlModel
from niffler_tests_python.model.enums.friendship_status import FriendshipAPIStatus


class UserModel(BaseModel):
    id: str
    username: str
    fullname: str | None = None
    currency: str

class UserName(BaseModel):
    username: str

class UserModelUpdate(BaseModel):
    id: str | None
    username: str | None
    fullname: str | None
    photo: str | None

class UserGqlResponse(BaseModel):
    id: str
    username: str
    fullname: str | None = None
    photo: str | None = None
    categories: list[CategoryGqlModel]

class UserDataGqlResponse(BaseModel):
    user: UserGqlResponse

class UserQueryGqlResponse(BaseModel):
    data: UserDataGqlResponse

class UserMutationResult(BaseModel):
    id: str
    username: str
    fullname: str | None = None
    photo: str | None = None

class UserMutationData(BaseModel):
    user:UserMutationResult

class UserMutationGqlResponse(BaseModel):
    data: UserMutationData

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
    firstname: str | None = None
    surname: str | None = None
    photo: bytes | None = None
    photo_small: bytes | None = None
    full_name: str | None = None
