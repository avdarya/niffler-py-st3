from pydantic import BaseModel


class CategoryGqlModel(BaseModel):
    id: str
    name: str
    username: str
    archived: bool
