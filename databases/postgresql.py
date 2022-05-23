from __future__ import annotations

from typing import Dict

import sqlalchemy as sa
from sqlalchemy import Column, Text
from sqlalchemy.dialects.postgresql import JSONB


class PostGreSQL:
    def __init__(self, uri, table_name='primary'):  # function to initialize the class
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

    def get_value(self, key):  # function to get a value from the database
        res = self.engine.execute(self.primary.select().where(self.primary.c.key == key)).fetchall()
        return res

    def __setitem__(self, key, value):  # redirect to the insert function
        return self.insert((key, value))

    def delete(self, key):  # function to delete a key value pair
        self.engine.execute(self.primary.delete().where(self.primary.c.key == key))

    def __delitem__(self, key):  # redirect to the delete function
        return self.delete(key)

    def insert(self, key_value: tuple | dict):  # function to insert a key value pair
        if isinstance(key_value, tuple):
            key, value = key_value
        elif isinstance(key_value, dict):
            def get_kv(d: Dict):  # get the first, key and value in a dict
                for key, value in d.items():
                    return key, value

            key, value = get_kv(key_value)
        else:
            raise TypeError("key_value must be a tuple or dict")
        self.engine.execute(self.primary.insert(), key=key, value=value)

    def close(self):  # function to close the connection
        self.db.dispose()
        self.engine.close()
