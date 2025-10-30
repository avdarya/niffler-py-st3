from pydantic import BaseModel

from niffler_tests_python.model.gql_model.category_gql import CategoryGqlModel


class UserGqlResponse(BaseModel):
    id: str
    username: str
    fullname: str | None = None
    photo: str | None = None
    categories: list[CategoryGqlModel]


class UserDataGqlResponse(BaseModel):
    user: UserGqlResponse


class UserQueryGqlResponse(BaseModel):
    data: UserDataGqlResponse


class UserMutationGqlResult(BaseModel):
    id: str
    username: str
    fullname: str | None = None
    photo: str | None = None


class UserMutationGqlData(BaseModel):
    user:UserMutationGqlResult


class UserMutationGqlResponse(BaseModel):
    data: UserMutationGqlData
