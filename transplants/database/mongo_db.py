import os

from pymongo import MongoClient
from pymongo.database import Database

CONNECTION_STRING_ENV_VAR_NAME = "MONGO_CONNECTION_STRING"
DEFAULT_CONNECTION_STRING = "mongodb://localhost:27017/"

KIDNEY_EXCHANGE_DATABASE_NAME_ENV_VAR_NAME = "MONGO_DATABASE_NAME"
DEFAULT_KIDNEY_EXCHANGE_DATABASE_NAME = "kidney_exchange"
TEST_KIDNEY_EXCHANGE_DATABASE_NAME = "kidney_exchange_test"

PROBLEMS_COLLECTION_NAME = "problem"
SOLUTIONS_COLLECTION_NAME = "solution"
SOLVER_CONFIG_COLLECTION_NAME = "solver_config"
JOB_COLLECTION_NAME = "job"

kidney_exchange_database_name = os.environ.get(KIDNEY_EXCHANGE_DATABASE_NAME_ENV_VAR_NAME,
                                               DEFAULT_KIDNEY_EXCHANGE_DATABASE_NAME)
connection_string = os.environ.get(CONNECTION_STRING_ENV_VAR_NAME, DEFAULT_CONNECTION_STRING)

mongo_client = MongoClient(connection_string)

kidney_exchange_database = mongo_client.get_database(kidney_exchange_database_name)

problem_collection = kidney_exchange_database.get_collection(PROBLEMS_COLLECTION_NAME)
solution_collection = kidney_exchange_database.get_collection(SOLUTIONS_COLLECTION_NAME)
solver_config_collection = kidney_exchange_database.get_collection(SOLVER_CONFIG_COLLECTION_NAME)
job_collection = kidney_exchange_database.get_collection(JOB_COLLECTION_NAME)


def initialize_db(database: Database):
    problem_collection = database.get_collection(PROBLEMS_COLLECTION_NAME)
    problem_collection.create_index("problem_id", unique=True)

    solution_collection = database.get_collection(SOLUTIONS_COLLECTION_NAME)
    solution_collection.create_index("solution_id", unique=True)

    solver_config_collection = database.get_collection(SOLVER_CONFIG_COLLECTION_NAME)
    solver_config_collection.create_index("solver_config_id", unique=True)

    job_collection = database.get_collection(JOB_COLLECTION_NAME)
    job_collection.create_index("job_id", unique=True)
