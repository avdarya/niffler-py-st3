from requests import Session, Response


class BaseSession(Session):

    __gateway_url: str | None
    __token: str | None

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self.__gateway_url = kwargs.get("gateway_url", None)
        self.__token = kwargs.get("token", None)
        self.headers.update({
            "Authorization": f"Bearer {self.__token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        })

    def request(self, method: str, path: str, **kwargs) -> Response:
        url = self.__gateway_url + path
        return super().request(method, url, **kwargs)