import allure
from allure_commons.types import AttachmentType
from requests import Session, Response
from requests_toolbelt.utils.dump import dump_response


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
        self.hooks['response'].append(self.attach_response)

    @staticmethod
    def attach_response(response: Response, *args, **kwargs):
        attachment_name = response.request.method + ' ' + response.request.url
        allure.attach(dump_response(response), attachment_name, attachment_type=AttachmentType.TEXT)

    def request(self, method: str, path: str, **kwargs) -> Response:
        url = self.__gateway_url + path
        return super().request(method, url, **kwargs)