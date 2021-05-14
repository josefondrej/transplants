from typing import Optional

from pymongo.database import Database

from transplants.database.mongo_db import kidney_exchange_database


class DatabaseMixin:
    db_id_name: str = None  # Name of the key that stores the identifier
    db_collection_name: str = None  # pymongo Collection name to use for loading / saving the data
    _database: Database = kidney_exchange_database

    @classmethod
    def get_collection(cls):
        collection = cls._database.get_collection(cls.db_collection_name)
        return collection

    def save_to_db(self):
        collection = self.get_collection()
        collection.insert_one(self.to_dict())

    def update_db(self, **kwargs):
        collection = self.get_collection()
        field_name, value = [(fn, v) for fn, v in kwargs.items()][0]
        collection.update_one(filter={self.db_id_name: getattr(self, self.db_id_name)},
                              update={"$set": {field_name: value}})

    @classmethod
    def find_by_id(cls, identifier: str) -> Optional["DatabaseMixin"]:
        collection = cls.get_collection()
        one = collection.find_one({cls.db_id_name: identifier})
        if one is None:
            return

        one.pop("_id")
        return cls.from_dict(one)

    @classmethod
    def set_database(cls, database: Database):
        cls._database = database
