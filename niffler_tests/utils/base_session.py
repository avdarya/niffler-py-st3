from requests import Session, Response


class BaseSession(Session):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self.base_url = kwargs.get("base_url", None)

    def request(self, method: str, path: str, **kwargs) -> Response:
        url = self.base_url + path
        return super().request(method, url, **kwargs)