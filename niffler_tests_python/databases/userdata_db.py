from sqlalchemy import Engine, create_engine
from sqlalchemy.engine import ScalarResult
from sqlmodel import Session, select

from niffler_tests_python.model.userdata import UserdataModelDB


class UserdataDB:

    engine: Engine

    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)

    def get_userdata_by_username(self, username: str) -> UserdataModelDB:
        with Session(self.engine) as session:
            statement = select(UserdataModelDB).where(UserdataModelDB.username == username)
            result: ScalarResult[UserdataModelDB] = session.exec(statement)
            return result.one()
