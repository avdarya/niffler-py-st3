from sqlmodel import SQLModel
from sqlalchemy import MetaData

auth_metadata = MetaData()
userdata_metadata = MetaData()

class AuthDBBase(SQLModel):
    metadata = auth_metadata

class UserdataDBBase(SQLModel):
    metadata = userdata_metadata