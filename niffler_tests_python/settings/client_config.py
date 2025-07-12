from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class ClientConfig(BaseSettings):
    username: str
    password: SecretStr

    model_config = SettingsConfigDict(
        env_file='.env',
        frozen=True,
        extra='ignore'
    )