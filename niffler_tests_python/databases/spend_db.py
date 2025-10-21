from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from typing import Sequence
from sqlalchemy import create_engine, Engine, event
from sqlmodel import select
from sqlalchemy import func

from niffler_tests_python.databases.base_db import BaseDB
from niffler_tests_python.model.category import CategoryModelDB
from niffler_tests_python.model.enums.currency_title import CurrencyTitle
from niffler_tests_python.model.enums.period_title import PeriodTitle
from niffler_tests_python.model.spend import SpendModelDB
from niffler_tests_python.settings.server_config import ServerConfig
from niffler_tests_python.utils.allure_helpers import attach_sql


class SpendDB(BaseDB):

    engine: Engine

    def __init__(self, server_config: ServerConfig):
        self.engine = create_engine(f'{server_config.spend_db_url}')
        event.listen(self.engine, 'do_execute', fn=attach_sql)

    def get_user_categories(self, username: str) -> Sequence[CategoryModelDB]:
        statement = select(CategoryModelDB).where(CategoryModelDB.username == username)
        return self.execute(self.engine, statement, 'all')

    def get_user_category_by_name(self, username: str, name: str) -> CategoryModelDB:
        statement = (select(CategoryModelDB)
                     .where(CategoryModelDB.username == username)
                     .where(CategoryModelDB.name == name))
        return self.execute(self.engine, statement, 'one_or_none')

    def get_category_by_id(self, category_id: str) -> CategoryModelDB:
        statement = select(CategoryModelDB).where(CategoryModelDB.id == category_id)
        return self.execute(self.engine, statement, 'one_or_none')

    def get_categories_by_id(self, category_ids: list[str] | set[str]) -> list[CategoryModelDB]:
        statement = select(CategoryModelDB).where(CategoryModelDB.id.in_(category_ids))
        return self.execute(self.engine, statement, 'all')

    def get_active_categories_by_id(self, category_ids: list[str] | set[str]) -> list[CategoryModelDB]:
        statement = (select(CategoryModelDB)
                     .where(CategoryModelDB.id.in_(category_ids))
                     .where(CategoryModelDB.archived == False))
        return self.execute(self.engine, statement, 'all')

    # def get_category_list(self) -> list[CategoryModelDB]:
    #     statement = select(CategoryModelDB)
    #     return self.execute(self.engine, statement, 'all')

    def delete_category(self, category_id: str):
        self.delete_records(self.engine, CategoryModelDB, CategoryModelDB.id == category_id)

    def get_spend(self, spend_id: str) -> SpendModelDB:
        statement = select(SpendModelDB).where(SpendModelDB.id == spend_id)
        return self.execute(self.engine, statement, 'one_or_none')

    def get_spend_list(self, spend_ids: list[str]) -> list[SpendModelDB]:
        statement = select(SpendModelDB).where(SpendModelDB.id.in_(spend_ids))
        return self.execute(self.engine, statement, 'all')

    def get_spend_by_filter(
            self, username: str,
            currency: CurrencyTitle | None = None,
            period: PeriodTitle | None = None
    ) -> list[SpendModelDB]:
        statement = select(SpendModelDB).where(SpendModelDB.username == username)

        if currency and currency != CurrencyTitle.ALL:
            statement = statement.where(SpendModelDB.currency == currency)

        if period and period != PeriodTitle.ALL_TIME:
            current_date = datetime.today()
            if period == PeriodTitle.TODAY:
                start_date = current_date.date()
            elif period == PeriodTitle.WEEK:
                start_date = (current_date - timedelta(days=7)).date()
            elif period == PeriodTitle.MONTH:
                start_date = (current_date - relativedelta(months=1)).date()
            else:
                start_date = None

            if start_date:
                statement = statement.where(SpendModelDB.spend_date >= start_date)

        return self.execute(self.engine, statement, "all")

    def get_spend_count(self) -> int:
        statement = select(func.count(SpendModelDB.id))
        return self.execute(self.engine, statement, 'one')
