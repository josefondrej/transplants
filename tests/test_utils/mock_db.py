from unittest import TestCase

import mongomock as mongomock

from transplants.database.database_mixin import DatabaseMixin
from transplants.database.mongo_db import DEFAULT_KIDNEY_EXCHANGE_DATABASE_NAME, kidney_exchange_database
from transplants.database.setup_db import setup_db

mock_mongo_client = mongomock.MongoClient()
mock_kidney_exchange_database = mock_mongo_client.get_database(DEFAULT_KIDNEY_EXCHANGE_DATABASE_NAME)


class MockDB(TestCase):
    def setUp(self) -> None:
        DatabaseMixin.set_database(mock_kidney_exchange_database)
        setup_db(database=mock_kidney_exchange_database, clean=True)

    def tearDown(self) -> None:
        setup_db(mock_kidney_exchange_database)
        DatabaseMixin.set_database(kidney_exchange_database)
