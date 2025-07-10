import base64
import hashlib
import os
import re
from requests import Session
from urllib.parse import urlparse, parse_qs


class AuthSession(Session):

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.code = None

    def request(self, method: str, url: str, **kwargs):
        response = super().request(method, url, **kwargs)
        for r in response.history:
            cookies = r.cookies.get_dict()
            self.cookies.update(cookies)

            code = parse_qs(urlparse(r.headers.get('Location')).query).get('code', None)
            if code:
                self.code = code

        return response

class AuthClient:

    def __init__(self, api_url: str):
        self.session = AuthSession()
        self.domain_url = api_url
        self.token = None

        self.code_verifier = base64.urlsafe_b64encode(os.urandom(32)).decode('utf-8')
        self.code_verifier = re.sub('[^a-zA-Z0-9]+', '', self.code_verifier)

        self.code_challenge = hashlib.sha256(self.code_verifier.encode('utf-8')).digest()
        self.code_challenge = base64.urlsafe_b64encode(self.code_challenge).decode('utf-8')
        self.code_challenge = self.code_challenge.replace('=', '')

    def auth(self, username: str, password: str) -> str:
        xsrf_response = self.session.get(
            url=f'{self.domain_url}/oauth2/authorize',
            params={
                'response_type': 'code',
                'client_id': 'client',
                'scope': 'openid',
                'redirect_uri': 'http://frontend.niffler.dc/authorized',
                'code_challenge': self.code_challenge,
                'code_challenge_method': 'S256'
            },
            allow_redirects=True
        )
        xsrf_response.raise_for_status()

        code_response = self.session.post(
            url=f'{self.domain_url}/login',
            data={
                'username': username,
                'password': password,
                '_csrf': self.session.cookies.get('XSRF-TOKEN'),
            },
            allow_redirects=True
        )
        code_response.raise_for_status()

        token_response = self.session.post(
            url=f'{self.domain_url}/oauth2/token',
            data={
                'code': self.session.code,
                'redirect_uri': 'http://frontend.niffler.dc/authorized',
                'code_verifier': self.code_verifier,
                'grant_type': 'authorization_code',
                'client_id': 'client'
            }
        )

        self.token = token_response.json().get('access_token', None)
        return self.token
