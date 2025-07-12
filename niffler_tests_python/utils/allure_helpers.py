import json
from json import JSONDecodeError

import allure
import curlify
import logging

from allure_commons.types import AttachmentType
from requests import Response


def allure_attach_request(function):
    """Декоратор логирования запросов/ответов в allure-step, allure-attachment, консоль."""

    def wrapper(*args, **kwargs):
        method, url = args[1], args[2]
        with allure.step(f'{method} {url}'):
            response: Response = function(*args, **kwargs)

            curl = curlify.to_curl(response.request)
            logging.debug(curl)
            logging.debug(response.text)

            allure.attach(
                body=curl.encode('utf-8'),
                name=f'Request {response.status_code}',
                attachment_type=AttachmentType.TEXT,
                extension='.txt'
            )
            try:
                allure.attach(
                    body=json.dumps(response.json(), indent=4).encode('utf-8'),
                    name=f'Response json {response.status_code}',
                    attachment_type=AttachmentType.JSON,
                    extension='.json'
                )
            except JSONDecodeError:
                allure.attach(
                    body=response.text.encode('utf-8'),
                    name=f'Response text {response.status_code}',
                    attachment_type=AttachmentType.TEXT,
                    extension='.txt'
                )
            allure.attach(
                body=json.dumps(dict(response.headers), indent=4).encode('utf-8'),
                attachment_type=AttachmentType.JSON,
                extension='.json'
            )

        return response

    return wrapper

def attach_sql(cursor, statement, parameters, context):
    statement_with_params = statement % parameters
    name = statement.split(' ')[0] + ' ' + context.engine.url.database
    allure.attach(statement_with_params, name=name, attachment_type=AttachmentType.TEXT)