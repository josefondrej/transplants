from pymongo.database import Database

from transplants.database.create_index import create_db_indices
from transplants.database.database_mixin import DatabaseMixin
from transplants.database.purge_db import purge_db


def setup_db(database: Database, clean: bool = False):
    DatabaseMixin.set_database(database=database)

    if clean:
        purge_db(database)

    create_db_indices(database)
