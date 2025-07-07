from typing import Sequence

import allure
from allure_commons.types import AttachmentType
from sqlalchemy import create_engine, Engine, event
from sqlmodel import Session, select
from sqlalchemy.engine import ScalarResult

from niffler_tests_python.model.category import CategoryModelDB
from niffler_tests_python.model.spend import SpendModelDB


class SpendDB:

    engine: Engine

    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        event.listen(self.engine, 'do_execute', self.attach_sql)

    @staticmethod
    def attach_sql(cursor, statement, parameters, context):
        statement_with_params = statement % parameters
        name = statement.split(' ')[0] + ' ' + context.engine.url.database
        allure.attach(statement_with_params, name=name, attachment_type=AttachmentType.TEXT)

    @allure.step('[DB] Get user categories: username={username}')
    def get_user_categories(self, username: str) -> Sequence[CategoryModelDB]:
        with Session(self.engine) as session:
            statement = select(CategoryModelDB).where(CategoryModelDB.username == username)
            result: ScalarResult[CategoryModelDB] = session.exec(statement)
            return result.all()

    @allure.step('[DB] Get category by name: name={name}')
    def get_category_by_name(self, name: str) -> CategoryModelDB:
        with Session(self.engine) as session:
            statement = select(CategoryModelDB).where(CategoryModelDB.name == name)
            result: ScalarResult[CategoryModelDB] = session.exec(statement)
            # return session.exec(statement).one()
            return result.one()

    @allure.step('[DB] Delete category: category_id={category_id}')
    def delete_category(self, category_id: str):
        with Session(self.engine) as session:
            category = session.get(CategoryModelDB, category_id)
            if category:
                session.delete(category)
                session.commit()

    @allure.step('[DB] Get spend: spend_id={spend_id}')
    def get_spend(self, spend_id: str) -> SpendModelDB:
        with Session(self.engine) as session:
            statement = select(SpendModelDB).where(SpendModelDB.id == spend_id)
            result: ScalarResult[SpendModelDB] = session.exec(statement)
            return result.one_or_none()