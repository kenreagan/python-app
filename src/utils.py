from collections.abc import MutableMapping
from abc import ABC
from sqlalchemy import insert, update, and_
from src.connector import DatabaseContext as DatabaseContextManager
from src.models import Base
from typing import Dict, Any

class DatabaseTableMixin(MutableMapping, ABC):

    def __init__(self, table: Base):
        self.table = table

    def __getitem__(self, item: int):
        with DatabaseContextManager() as contextmanager:
            response = contextmanager.session.query(self.table).filter_by(
                id=item
            ).first()
        return response

    def __create_item__(self, value: Dict[str, Any]):
        with DatabaseContextManager() as contextmanager:
            statement = insert(self.table).values(
                **value
            )
            try:
                contextmanager.session.execute(statement)
                contextmanager.commit()
            except Exception as e:
                print(f"{e!r}")
            finally:
                contextmanager.commit()

    def __setitem__(self, key, value: Dict[str, str]) -> Dict[str, str]:
        with DatabaseContextManager() as contextmanager:
            statement = update(self.table).where(
                self.table.id == key
            ).values(**value)
            contextmanager.session.execute(statement)
            contextmanager.commit()
        return value

    def __len__(self) -> int:
        with DatabaseContextManager() as contextmanager:
            return contextmanager.session.query(self.table).filter_by().count()

    def __iter__(self):
        with DatabaseContextManager() as contextmanager:
            for elements in contextmanager.session.query(self.table):
                yield elements

    def __delitem__(self, key):
        instance = self[key]
        print(instance)
        with DatabaseContextManager() as contextmanager:
            contextmanager.session.delete(instance)
            contextmanager.commit()

    def filter(self, **kwargs):
        with DatabaseContextManager() as contextmanager:
            return contextmanager.session.query(self.table).filter_by(**kwargs)

    def filtername(self, name):
        with DatabaseContextManager() as contextmanager:
            return contextmanager.session.query(self.table).filter(self.table.name.contains(name))
    
    def __contains__(self, name) -> bool:
        for elements in iter(self):
            if elements.name == name:
                return True
            return False
