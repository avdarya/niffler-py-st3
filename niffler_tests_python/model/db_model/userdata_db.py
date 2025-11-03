from sqlmodel import Field

from niffler_tests_python.model.db_model._bases import UserdataDBBase


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
