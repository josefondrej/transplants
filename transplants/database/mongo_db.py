import os

from pymongo import MongoClient

CONNECTION_STRING_ENV_VAR_NAME = "MONGO_CONNECTION_STRING"
DEFAULT_CONNECTION_STRING = "mongodb://localhost:27017/"

KIDNEY_EXCHANGE_DATABASE_NAME_ENV_VAR_NAME = "MONGO_DATABASE_NAME"
DEFAULT_KIDNEY_EXCHANGE_DATABASE_NAME = "kidney_exchange"
TEST_KIDNEY_EXCHANGE_DATABASE_NAME = "kidney_exchange_test"

PROBLEMS_COLLECTION_NAME = "problem"
SOLUTIONS_COLLECTION_NAME = "solution"

kidney_exchange_database_name = os.environ.get(KIDNEY_EXCHANGE_DATABASE_NAME_ENV_VAR_NAME,
                                               DEFAULT_KIDNEY_EXCHANGE_DATABASE_NAME)
connection_string = os.environ.get(CONNECTION_STRING_ENV_VAR_NAME, DEFAULT_CONNECTION_STRING)

mongo_client = MongoClient(connection_string)

kidney_exchange_database = mongo_client.get_database(kidney_exchange_database_name)

problem_collection = kidney_exchange_database.get_collection(PROBLEMS_COLLECTION_NAME)
solution_collection = kidney_exchange_database.get_collection(SOLUTIONS_COLLECTION_NAME)
