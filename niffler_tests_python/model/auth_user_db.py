from sqlmodel import Field

from niffler_tests_python.model._bases import AuthDBBase


class AuthUserModelDB(AuthDBBase, table=True):
    __tablename__ = "user"

    id: str = Field(default=None, primary_key=True)
    username: str
    password: str
    enabled: bool
    account_non_expired: bool
    account_non_locked: bool
    credentials_non_expired: bool
