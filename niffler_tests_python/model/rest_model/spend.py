from datetime import datetime

from pydantic import BaseModel

from niffler_tests_python.model.rest_model.category import CategoryModel

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

class SpendModelEdit(BaseModel):
    id: str
    amount: float
    description: str
    currency: str
    spendDate: str
    category: dict
