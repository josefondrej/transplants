from unittest import TestCase

from transplants.database.mongo_db import kidney_exchange_database
from transplants.database.setup_db import setup_db


class MockDB(TestCase):
    def setUp(self) -> None:
        setup_db(database=kidney_exchange_database, clean=True)

    def tearDown(self) -> None:
        setup_db(kidney_exchange_database)
