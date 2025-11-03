from pydantic_settings import BaseSettings, SettingsConfigDict


class GRPCConfig(BaseSettings):
    currency_service_host: str
    currency_wiremock_host: str

    model_config = SettingsConfigDict(
        env_file='.env',
        frozen=True,
        extra='ignore'
    )
