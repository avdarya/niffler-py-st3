import allure
from niffler_tests_python.model.userdata import UserModel, UserModelUpdate, UserFriendshipModel, UserName
from niffler_tests_python.utils.sessions import BaseSession


class UserApiClient:

    session: BaseSession

    def __init__(self, session: BaseSession) -> None:
        self.session = session

    def get_current_user(self) -> UserModel:
        response = self.session.get("/api/users/current")
        return UserModel.model_validate(response.json())

    def update_name(self, userdata: UserModelUpdate) -> UserModel:
        response = self.session.post(
            "/api/users/update",
            json=userdata.model_dump(),
        )
        return UserModel.model_validate(response.json())

    def get_users_all(
            self,
            page: int = 0,
            search_query: str = None,
            sort: str = 'username,ASC'
    ) -> dict:
        params = {
            "page": page,
            "searchQuery": search_query,
            "sort": sort
        }
        response = self.session.get(
            '/api/v2/users/all',
            params=params,
        )
        return response.json()

    def get_friends_all(
            self,
            page: int = 0,
            search_query: str = None,
            sort: str = 'username,ASC'
    ) -> dict:
        params = {
            "page": page,
            "searchQuery": search_query,
            "sort": sort
        }
        response = self.session.get(
            '/api/v2/friends/all',
            params=params,
        )
        return response.json()

    def send_invitation(self, username: UserName) -> UserFriendshipModel:
        response = self.session.post(
            '/api/invitations/send',
            json=username.model_dump()
        )
        return UserFriendshipModel.model_validate(response.json())

    def accept_invitation(self, username: UserName) -> UserFriendshipModel:
        response = self.session.post(
            '/api/invitations/accept',
            json=username.model_dump()
        )
        return UserFriendshipModel.model_validate(response.json())

    def decline_invitation(self, username: UserName) -> UserFriendshipModel:
        response = self.session.post(
            '/api/invitations/decline',
            json=username.model_dump()
        )
        return UserFriendshipModel.model_validate(response.json())