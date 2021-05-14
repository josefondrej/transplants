from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask import Flask
from flask_apispec import FlaskApiSpec
from flask_restful import Api

from transplants.api.job_processing import start_job_processing
from transplants.database.initialize_db import initialize_db
from transplants.database.mongo_db import kidney_exchange_database
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

if __name__ == '__main__':
    # purge_db(kidney_exchange_database) # Uncomment for testing
    initialize_db(kidney_exchange_database)
    start_job_processing()
    app.run(port=5000, debug=True)
