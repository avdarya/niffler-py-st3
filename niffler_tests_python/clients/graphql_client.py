from niffler_tests_python.model.gql_model.stat_gql import StatisticsGqlResponse
from niffler_tests_python.model.gql_model.user_gql import UserQueryGqlResponse, UserMutationGqlResponse
from niffler_tests_python.utils.sessions import GraphqlSession


class GraphQLClient:

    session: GraphqlSession

    def __init__(self, session: GraphqlSession):
        self.session = session

    def query_stat(self, query: str, variables: dict | None = None) -> StatisticsGqlResponse:
        return self._execute(query, variables, StatisticsGqlResponse)

    def query_user(self, query: str, variables: dict | None = None) -> UserQueryGqlResponse:
        return self._execute(query, variables, UserQueryGqlResponse)

    def mutation_user(self, query: str, variables: dict | None = None) -> UserMutationGqlResponse:
        return self._execute(query, variables, UserMutationGqlResponse)

    def _execute(self, query: str, variables: dict | None, model):
        response = self.session.post(
            "/graphql",
            json={
                "query": query,
                "variables": variables or {},
            }
        )
        return model.model_validate(response.json())