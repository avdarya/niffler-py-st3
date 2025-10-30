from datetime import datetime

from sqlmodel import SQLModel, Field


class SpendModelDB(SQLModel, table=True):
    __tablename__ = "spend"

    id: str = Field(default=None, primary_key=True)
    amount: float
    description: str
    category_id: str
    username: str
    spend_date: datetime
    currency: str
