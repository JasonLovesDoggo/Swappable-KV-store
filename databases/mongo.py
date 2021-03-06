from __future__ import annotations

from typing import Dict, List

import pymongo

from databases.Base import DatabaseStats


class Collection:
    def __init__(self, client, collection):
        self.client = client
        self.collection = collection

    def get_value(self, key):
        return self.collection.find_one({"key": key})

    def insert(self, data: Dict):
        self.collection.insert(data)

    def insert_many(self, data: List[Dict] | Dict):
        self.collection.insert_many(data)

    def delete(self, key):
        self.collection.delete({"key": key})

    def exists(self, key):
        return self.collection.exists({"key": key})

    def database(self):
        return super(self)


class MongoDB(DatabaseStats):
    def __init__(self, uri):
        super().__init__()
        self.client = pymongo.MongoClient(uri)['primary']  # self.AddTable("test")['pizza'].insert({"name": "test"})

    def __getitem__(self, key):  # returns the database of the given name
        return Collection(self.client, self.client[key])

    def __add__(self, other):
        return self.AddTable(other)

    def AddTable(self, TableName):
        db_table = self.client[TableName]
        return Collection(self.client, db_table)

    def close(self):
        self.client.close()
