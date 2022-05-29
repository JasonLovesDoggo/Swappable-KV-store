from __future__ import annotations

from typing import Dict

import sqlalchemy as sa
from sqlalchemy import Column, Text, select
from sqlalchemy.dialects.postgresql import JSONB

from databases.Base import DatabaseStats


class PostGreSQL(DatabaseStats):
    def __init__(self, uri, table_name='primary'):  # function to initialize the class
        super().__init__()
        self.uri = uri
        self.db = sa.create_engine(uri)
        self.engine = self.db.connect()
        self.meta = sa.MetaData(self.engine)

        key_col = Column('key', Text, primary_key=True)
        value_col = Column('value', JSONB)
        self.primary = sa.Table(table_name, self.meta, key_col, value_col)
        self.meta.create_all()

    def __getitem__(self, arg):
        return PostGreSQL(self.uri, table_name=arg)

    def get(self, key):  # function to get a value from the database
        try:
            res = self.engine.execute(self.primary.select().where(self.primary.c.key == key)).fetchone()[1]
            return res
        except Exception:
            return None

    def __setitem__(self, key, value):  # redirect to the insert function
        return self.insert((key, value))

    def delete(self, key):  # function to delete a key value pair
        self.engine.execute(self.primary.delete().where(self.primary.c.key == key))

    def __delitem__(self, key):  # redirect to the delete function
        return self.delete(key)

    def exists(self, key):  # function to check if a key exists
        return select(self.primary.columns).where(self.primary.c.key == key).execute().fetchone() is not None

    def insert(self, key_value: tuple | dict):  # function to insert a key value pair
        key, value = unpack(key_value)
        self.engine.execute(self.primary.insert(), key=key, value=value)

    def close(self):  # function to close the connection
        self.db.dispose()
        self.engine.close()

def unpack(key_value: tuple | dict):  # function to unpack a tuple or dict
    if isinstance(key_value, tuple):
        key, value = key_value
        return key, value
    elif isinstance(key_value, dict):
        def get_kv(d: Dict):  # get the first, key and value in a dict
            for key, value in d.items():
                return key, value
        return get_kv(key_value)
    else:
        raise TypeError("key_value must be a tuple or dict")
