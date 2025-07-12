from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import HttpUrl, PostgresDsn, PositiveFloat
from typing import Literal


class ServerConfig(BaseSettings):
    frontend_url: HttpUrl
    gateway_url: HttpUrl
    auth_url: HttpUrl

    spend_db_url: PostgresDsn
    userdata_db_url: PostgresDsn

    timeout: PositiveFloat = 5.0
    poll: PositiveFloat = 0.5
    browser_name: Literal['chrome', 'firefox'] = 'chrome'

    model_config = SettingsConfigDict(
        env_file='.env',
        frozen=True,
        extra='ignore'
    )