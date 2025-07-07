import allure
from allure_commons.types import AttachmentType
from sqlalchemy import Engine, create_engine, event
from sqlalchemy.engine import ScalarResult
from sqlmodel import Session, select

from niffler_tests_python.model.userdata import UserdataModelDB


class UserdataDB:

    engine: Engine

    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        event.listen(self.engine, 'do_execute', self.attach_sql)

    @staticmethod
    def attach_sql(cursor, statement, parameters, context):
        statement_with_params = statement % parameters
        name = statement.split(' ')[0] + ' ' + context.engine.url.database
        allure.attach(statement_with_params, name, attachment_type=AttachmentType.TEXT)

    @allure.step('[DB] Get userdata: username={username}')
    def get_userdata_by_username(self, username: str) -> UserdataModelDB:
        with Session(self.engine) as session:
            statement = select(UserdataModelDB).where(UserdataModelDB.username == username)
            result: ScalarResult[UserdataModelDB] = session.exec(statement)
            return result.one()
