from typing import Sequence

from sqlalchemy import create_engine, Engine
from sqlmodel import Session, select
from sqlalchemy.engine import ScalarResult

from niffler_tests_python.model.category import CategoryModelDB
from niffler_tests_python.model.spend import SpendModelDB


class SpendDB:

    engine: Engine

    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)

    def get_user_categories(self, username: str) -> Sequence[CategoryModelDB]:
        with Session(self.engine) as session:
            statement = select(CategoryModelDB).where(CategoryModelDB.username == username)
            result: ScalarResult[CategoryModelDB] = session.exec(statement)
            # return session.exec(statement).all()
            return result.all()

    def get_category_by_name(self, name: str) -> CategoryModelDB:
        with Session(self.engine) as session:
            statement = select(CategoryModelDB).where(CategoryModelDB.name == name)
            result: ScalarResult[CategoryModelDB] = session.exec(statement)
            # return session.exec(statement).one()
            return result.one()

    def delete_category(self, category_id: str):
        with Session(self.engine) as session:
            category = session.get(CategoryModelDB, category_id)
            if category:
                session.delete(category)
                session.commit()

    def get_spend(self, spend_id: str) -> SpendModelDB:
        with Session(self.engine) as session:
            statement = select(SpendModelDB).where(SpendModelDB.id == spend_id)
            result: ScalarResult[SpendModelDB] = session.exec(statement)
            return result.one_or_none()