import allure
from niffler_tests_python.model.userdata import UserdataModel, UserdataModelUpdate
from niffler_tests_python.utils.sessions import BaseSession


class UserApiClient:

    session: BaseSession

    def __init__(self, session: BaseSession) -> None:
        self.session = session

    @allure.step('[API] Get current user')
    def get_current_user(self) -> UserdataModel:
        response = self.session.get("/api/users/current")
        return UserdataModel.model_validate(response.json())

    @allure.step('[API] Update user: userdata={userdata}')
    def update_name(self, userdata: UserdataModelUpdate) -> UserdataModel:
        response = self.session.post(
            "/api/users/update",
            json=userdata.model_dump(),
        )
        return UserdataModel.model_validate(response.json())