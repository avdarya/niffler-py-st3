from pydantic import BaseModel
from sqlmodel import SQLModel, Field

class CategoryModel(BaseModel):
    id: str
    name: str
    username: str
    archived: bool

class CategoryModelDB(SQLModel, table=True):
    __tablename__ = "category"

    id: str = Field(default=None, primary_key=True)
    name: str
    username: str
    archived: bool