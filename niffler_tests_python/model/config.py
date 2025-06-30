from pydantic import BaseModel


class Envs(BaseModel):
    frontend_url: str
    # gateway_url: str
    spend_db_url: str
    userdata_db_url: str
    username: str
    password: str
