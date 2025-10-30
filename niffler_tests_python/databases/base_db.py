from sqlalchemy import ScalarResult
from sqlmodel import Session, select

from niffler_tests_python.model.db_model.userdata_db import UserModelDB


class BaseDB:

    def execute(self, engine, statement, fetch: str = 'one'):
        with Session(engine) as session:
            result = session.exec(statement)

            if fetch == "all":
                return result.all()
            elif fetch == "one":
                return result.one()
            elif fetch == "one_or_none":
                return result.one_or_none()
            else:
                return result

    def insert_record(self, engine, model_instance):
        with Session(engine) as session:
            session.add(model_instance)
            session.commit()
            session.refresh(model_instance)
            return model_instance

    def delete_records(self, engine, model, *filter_expression):
        with Session(engine) as session:
            statement = select(model)
            for expr in filter_expression:
                statement = statement.where(expr)

            result: ScalarResult[UserModelDB] = session.exec(statement)
            records = result.all()
            for record in records:
                session.delete(record)
            session.commit()