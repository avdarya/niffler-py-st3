from typing import Optional
from pydantic import BaseModel
from sqlmodel import SQLModel, Field


class UserdataModel(BaseModel):
    id: str
    username: str
    fullname: str
    currency: str

class UserName(BaseModel):
    username: str

class UserdataModelUpdate(BaseModel):
    id: str | None
    username: str | None
    fullname: str | None
    photo: str | None

class UserdataModelDB(SQLModel, table=True):
    __tablename__ = "user"

    id: str = Field(default=None, primary_key=True)
    username: str
    currency: str
    firstname: Optional[str]
    surname: Optional[str]
    photo: Optional[bytes]
    photo_small: Optional[bytes]
    full_name: Optional[str]
