from sqlalchemy import Engine, create_engine, event

from niffler_tests_python.databases.base_db import BaseDB
from niffler_tests_python.settings.server_config import ServerConfig
from niffler_tests_python.utils.allure_helpers import attach_sql


class UserdataBaseDB(BaseDB):

    engine: Engine

    def __init__(self, server_config: ServerConfig):
        self.engine = create_engine(f'{server_config.userdata_db_url}')
        event.listen(self.engine, 'do_execute', fn=attach_sql)
