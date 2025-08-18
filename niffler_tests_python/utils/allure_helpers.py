import json
from json import JSONDecodeError

import allure
import curlify
import logging
import os
from jinja2 import Environment, FileSystemLoader, select_autoescape
from allure_commons.types import AttachmentType
from requests import Response, PreparedRequest, Request
from requests.cookies import merge_cookies, RequestsCookieJar
from requests.sessions import merge_hooks, merge_setting
from requests.structures import CaseInsensitiveDict


template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
template_dir = os.path.abspath(template_dir)

def allure_attach_request(function):
    """Декоратор логирования запросов/ответов в allure-step, allure-attachment, консоль."""

    def wrapper(*args, **kwargs):
        self_ = args[0]
        method, url = args[1], args[2]

        # with jinja2 -->
        headers = kwargs.get('headers', None)
        files = kwargs.get('files', None)
        data = kwargs.get('data', None)
        params = kwargs.get('params', None)
        auth = kwargs.get('auth', None)
        cookies = kwargs.get('cookies', None)
        hooks = kwargs.get('hooks', None)
        json_ = kwargs.get('json', None)
        request = Request(
            method=method.upper(),
            url=f'{getattr(self_, "gateway_url", getattr(self_, "auth_url", ""))}' + url,
            headers=headers,
            files=files,
            data=data or {},
            json=json_,
            params=params or {},
            auth=auth,
            cookies=cookies,
            hooks=hooks,
        )
        prepared_request = PreparedRequest()
        prepared_request.prepare(
            method=request.method.upper(),
            url=request.url,
            files=request.files,
            data=request.data,
            json=request.json,
            headers=merge_setting(
                request.headers, self_.headers, dict_class=CaseInsensitiveDict
            ),
            params=merge_setting(request.params, self_.params),
            auth=merge_setting(auth, self_.auth),
            cookies=merge_cookies(
                merge_cookies(RequestsCookieJar(), self_.cookies), cookies
            ),
            hooks=merge_hooks(request.hooks, self_.hooks),
        )
        new_env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape()
        )
        template_request = new_env.get_template('http-request.ftl')
        template_response = new_env.get_template('http-response.ftl')
        # <-- with jinja2

        with allure.step(f'{method} {url}'):

            response: Response = function(*args, **kwargs)

            curl = curlify.to_curl(response.request)
            logging.debug(curl)
            logging.debug(response.text)

            # jinja2 request -->
            rendered_request = template_request.render(
                request=prepared_request,
                curl=curl
            )
            allure.attach(
                body=rendered_request,
                name=f'Request {method} {url}',
                attachment_type=AttachmentType.HTML,
                extension='.html'
            )
            # <-- jinja2 request

            # jinja2 response -->
            response_data = {
                'responseCode': response.status_code,
                'url': response.url,
                'headers': {k: str(v) for k, v in response.headers.items()},
                'cookies': {k: str(v) for k, v in response.cookies.items()}
            }

            try:
                response_data['body'] = json.dumps(response.json(), indent=4)
            except JSONDecodeError:
                response_data['body'] = response.text

            rendered_response = template_response.render(
                data=response_data,
            )

            allure.attach(
                body=rendered_response,
                name=f'Response {response.status_code}',
                attachment_type=AttachmentType.HTML,
                extension='.html'
            )
            # <-- jinja2 response



            # without jinja2
            # allure.attach(
            #     body=curl.encode('utf-8'),
            #     name=f'Request {response.status_code}',
            #     attachment_type=AttachmentType.TEXT,
            #     extension='.txt'
            # )
            # try:
            #     allure.attach(
            #         body=json.dumps(response.json(), indent=4).encode('utf-8'),
            #         name=f'Response json {response.status_code}',
            #         attachment_type=AttachmentType.JSON,
            #         extension='.json'
            #     )
            # except JSONDecodeError:
            #     allure.attach(
            #         body=response.text.encode('utf-8'),
            #         name=f'Response text {response.status_code}',
            #         attachment_type=AttachmentType.TEXT,
            #         extension='.txt'
            #     )
            # allure.attach(
            #     body=json.dumps(dict(response.headers), indent=4).encode('utf-8'),
            #     name = f"Response headers {response.status_code}",
            #     attachment_type=AttachmentType.JSON,
            #     extension='.json'
            # )

        return response

    return wrapper

def attach_sql(cursor, statement, parameters, context):
    statement_with_params = statement % parameters
    name = statement.split(' ')[0] + ' ' + context.engine.url.database
    allure.attach(statement_with_params, name=name, attachment_type=AttachmentType.TEXT)



# import json
# from json import JSONDecodeError
#
# import allure
# import curlify
# import logging
#
# from allure_commons.types import AttachmentType
# from requests import Response
#
#
# def allure_attach_request(function):
#     """Декоратор логирования запросов/ответов в allure-step, allure-attachment, консоль."""
#
#     def wrapper(*args, **kwargs):
#         method, url = args[1], args[2]
#         with allure.step(f'{method} {url}'):
#             response: Response = function(*args, **kwargs)
#
#             curl = curlify.to_curl(response.request)
#             logging.debug(curl)
#             logging.debug(response.text)
#
#             allure.attach(
#                 body=curl.encode('utf-8'),
#                 name=f'Request {response.status_code}',
#                 attachment_type=AttachmentType.TEXT,
#                 extension='.txt'
#             )
#             try:
#                 allure.attach(
#                     body=json.dumps(response.json(), indent=4).encode('utf-8'),
#                     name=f'Response json {response.status_code}',
#                     attachment_type=AttachmentType.JSON,
#                     extension='.json'
#                 )
#             except JSONDecodeError:
#                 allure.attach(
#                     body=response.text.encode('utf-8'),
#                     name=f'Response text {response.status_code}',
#                     attachment_type=AttachmentType.TEXT,
#                     extension='.txt'
#                 )
#             allure.attach(
#                 body=json.dumps(dict(response.headers), indent=4).encode('utf-8'),
#                 attachment_type=AttachmentType.JSON,
#                 extension='.json'
#             )
#
#         return response
#
#     return wrapper
#
# def attach_sql(cursor, statement, parameters, context):
#     statement_with_params = statement % parameters
#     name = statement.split(' ')[0] + ' ' + context.engine.url.database
#     allure.attach(statement_with_params, name=name, attachment_type=AttachmentType.TEXT)