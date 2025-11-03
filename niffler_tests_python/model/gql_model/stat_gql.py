from datetime import datetime

from pydantic import BaseModel


class StatByCategoryGqlResponse(BaseModel):
    categoryName: str
    currency: str
    sum: float
    firstSpendDate: datetime
    lastSpendDate: datetime

class StatGqlResponse(BaseModel):
    total: float
    currency: str
    statByCategories: list[StatByCategoryGqlResponse]

class DataGqlResponse(BaseModel):
    stat: StatGqlResponse

class StatisticsGqlResponse(BaseModel):
    data: DataGqlResponse