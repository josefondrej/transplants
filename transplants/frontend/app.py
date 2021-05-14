import argparse

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask import Flask
from flask_apispec import FlaskApiSpec
from flask_restful import Api
from pymongo.database import Database

from transplants.api.job_processing import start_job_processing
from transplants.database.mongo_db import kidney_exchange_database, kidney_exchange_database_test
from transplants.database.setup_db import setup_db
from transplants.frontend.resources.job import Job
from transplants.frontend.resources.jobs import Jobs
from transplants.frontend.resources.problem import Problem
from transplants.frontend.resources.solution import Solution
from transplants.frontend.resources.solver_config import SolverConfig

app = Flask(__name__)

api = Api(app)

api.add_resource(Problem, "/problem/<string:problem_id>")
api.add_resource(SolverConfig, "/solver_config/<string:solver_config_id>")
api.add_resource(Solution, "/solution/<string:solution_id>")
api.add_resource(Job, "/job/<string:job_id>")
api.add_resource(Jobs, "/jobs/")

app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Kidney Exchange Problem Solver',
        version='1.0.0',
        openapi_version='2.0',
        plugins=[MarshmallowPlugin()],
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',
})

docs = FlaskApiSpec(app)

docs.register(Problem)
docs.register(SolverConfig)
docs.register(Solution)
docs.register(Job)
docs.register(Jobs)


def start_app(database: Database, host: str = "localhost", port: int = 5000, debug: bool = True):
    setup_db(database=database, clean=True)
    start_job_processing()
    app.run(host=host, port=port, debug=debug)


def start_app_with_args():
    parser = argparse.ArgumentParser(description="Transplants Solve API")
    parser.add_argument("--mode", default="test", required=False, help="Run in test mode",
                        choices=["test", "production"])

    args = parser.parse_args()

    run_in_production_mode = (args.mode == "production")

    if run_in_production_mode:
        print("Running in production mode")
        start_app(database=kidney_exchange_database)

    else:
        print("Running in test mode")
        start_app(database=kidney_exchange_database_test)


if __name__ == '__main__':
    start_app_with_args()
