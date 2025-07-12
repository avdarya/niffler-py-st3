from typing import Sequence
import allure
from sqlalchemy import create_engine, Engine, event
from sqlmodel import Session, select
from sqlalchemy.engine import ScalarResult
from sqlalchemy import func

from niffler_tests_python.model.category import CategoryModelDB
from niffler_tests_python.model.spend import SpendModelDB
from niffler_tests_python.settings.server_config import ServerConfig
from niffler_tests_python.utils.allure_helpers import attach_sql


class SpendDB:

    engine: Engine

    def __init__(self, server_config: ServerConfig):
        self.engine = create_engine(f'{server_config.spend_db_url}')
        event.listen(self.engine, 'do_execute', fn=attach_sql)

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
            return result.one_or_none()

    @allure.step('[DB] Get category by category_id: category_id={category_id}')
    def get_category_by_id(self, category_id: str) -> CategoryModelDB:
        with Session(self.engine) as session:
            return session.get(CategoryModelDB, category_id)

    @allure.step('[DB] Get all categories')
    def get_category_list(self) -> list[CategoryModelDB]:
        with Session(self.engine) as session:
            statement = select(CategoryModelDB)
            result: ScalarResult[list[CategoryModelDB]] = session.exec(statement)
            return result.all()

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

    @allure.step('[DB] Set spend list: spend_ids={spend_ids}')
    def get_spend_list(self, spend_ids: list[str]) -> list[SpendModelDB]:
        with Session(self.engine) as session:
            statement = select(SpendModelDB).where(SpendModelDB.id.in_(spend_ids))
            result: ScalarResult[list[SpendModelDB]] = session.exec(statement)
            return result.all()

    @allure.step('[DB] Get spending count')
    def get_spend_count(self) -> int:
        with Session(self.engine) as session:
            statement = select(func.count(SpendModelDB.id))
            result: ScalarResult[int] = session.exec(statement)
            return result.one()