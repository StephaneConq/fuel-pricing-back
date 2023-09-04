from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import text
import os

connection_string = os.environ.get("SQL_CONNECTION_STRING")


class DBUtil:
    instance_ = None
    Base = None
    engine = None
    Session = None
    session = None

    def __new__(cls):
        if not isinstance(cls.instance_, cls):
            print("creating new instances")
            cls._instance = object.__new__(cls)
            cls.Base = declarative_base()
            cls.engine = create_engine(
                connection_string,
                connect_args={"options": "-csearch_path=core"},
                pool_size=20,
                max_overflow=0,
            )
            cls.Base.metadata.create_all(cls._instance.engine)
            cls.Session = sessionmaker(bind=cls._instance.engine)
            cls.session = cls._instance.Session()

        return cls._instance

    def delete_all(self, table):
        with self.engine.connect() as con:
            rs = con.execute(text(f"DELETE FROM {table} where 1 = 1"))
            con.commit()

    def bulk_save(self, items):
        self.session.bulk_save_objects(items)
        self.session.commit()

    def list_all(self, model):
        items = self.session.query(model).all()
        return list(map(lambda i: i.as_dict(), items))
