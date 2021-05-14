from unittest import TestCase

from transplants.database.database_mixin import DatabaseMixin
from transplants.database.initialize_db import initialize_db
from transplants.database.mongo_db import kidney_exchange_database_test, kidney_exchange_database
from transplants.database.purge_db import purge_db


class MockDB(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        purge_db(database=kidney_exchange_database_test)
        initialize_db(database=kidney_exchange_database_test)
        DatabaseMixin.set_database(kidney_exchange_database_test)

    @classmethod
    def tearDownClass(cls) -> None:
        purge_db(database=kidney_exchange_database_test)
        DatabaseMixin.set_database(kidney_exchange_database)
