from requests import Response

from niffler_tests.utils.base_session import BaseSession


class UserApiClient:

    session: BaseSession

    def __init__(self, session: BaseSession) -> None:
        self.session = session

    def get_current_user(self) -> Response:
        return self.session.get("/api/users/current")

    def update_name(self, user: dict) -> Response:
        return self.session.post(
            "/api/users/update",
            json=user,
        )