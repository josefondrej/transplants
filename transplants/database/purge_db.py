from pymongo.database import Database

from transplants.database.mongo_db import kidney_exchange_database


def purge_db(database: Database):
    collection_names = database.list_collection_names()
    for collection_name in collection_names:
        database.drop_collection(name_or_collection=collection_name)


if __name__ == '__main__':
    purge_db(kidney_exchange_database)
