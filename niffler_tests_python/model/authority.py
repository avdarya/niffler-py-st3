from sqlmodel import SQLModel
from sqlmodel import Field


class AuthorityModelDB(SQLModel, table=True):
    __tablename__ = "authority"

    id: str = Field(default=None, primary_key=True)
    user_id: str
    authority: str