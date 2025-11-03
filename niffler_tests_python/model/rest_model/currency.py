from pydantic import BaseModel


class CurrencyModel(BaseModel):
    currency: str
    currencyRate: float