from pydantic import BaseModel

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

class UserFriendshipModel(BaseModel):
    id: str
    username: str
    currency: str
    friendshipStatus: FriendshipAPIStatus | None = None
    fullname: str | None = None
