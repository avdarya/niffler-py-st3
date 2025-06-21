import dotenv
import os

from requests import Response
from utils.base_session import BaseSession

class UserApiClient:

    def __init__(self, session: BaseSession) -> None:
        self.session = session

    def get_token(self) -> str:
        dotenv.load_dotenv()
        token = os.getenv("TOKEN")
        return token

    def get_current_user(self) -> Response:
        headers = {'Authorization': f"Bearer {self.get_token()}"}
        return self.session.get("/api/users/current", headers=headers)