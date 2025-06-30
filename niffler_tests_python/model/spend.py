from datetime import datetime

from pydantic import BaseModel
from sqlmodel import SQLModel, Field

from niffler_tests_python.model.category import CategoryModel

class SpendModel(BaseModel):
    id: str
    amount: float
    description: str
    category: CategoryModel
    username: str
    spendDate: datetime
    currency: str

class SpendModelAdd(BaseModel):
    amount: float
    description: str
    currency: str
    spendDate: str
    category: dict

class SpendModelDB(SQLModel, table=True):
    __tablename__ = "spend"

    id: str = Field(default=None, primary_key=True)
    amount: float
    description: str
    category_id: str
    username: str
    spend_date: datetime
    currency: str