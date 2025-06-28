from requests import Session, Response


class BaseSession(Session):

    __base_url: str | None
    __token: str | None

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self.__base_url = kwargs.get("base_url", None)
        self.__token = kwargs.get("token", None)
        self.headers.update({
            "Authorization": f"Bearer {self.__token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        })

    def request(self, method: str, path: str, **kwargs) -> Response:
        url = self.__base_url + path
        return super().request(method, url, **kwargs)