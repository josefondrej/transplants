from pymongo.database import Database


def purge_db(database: Database):
    collection_names = database.list_collection_names()
    for collection_name in collection_names:
        database.drop_collection(name_or_collection=collection_name)
