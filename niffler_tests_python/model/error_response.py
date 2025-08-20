from pydantic import BaseModel


class ErrorResponseModel(BaseModel):
    type: str
    title: str
    status: int
    detail: str
    instance: str
