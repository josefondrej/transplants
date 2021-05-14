from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask import Flask
from flask_apispec import FlaskApiSpec
from flask_restful import Api
from pymongo.database import Database

from transplants.api.job_processing import start_job_processing
from transplants.database.mongo_db import kidney_exchange_database
from transplants.database.setup_db import setup_db
from transplants.frontend.resources.job_resource import JobResource
from transplants.frontend.resources.jobs_resource import JobsResource
from transplants.frontend.resources.patient_resource import PatientResource
from transplants.frontend.resources.problem_resource import ProblemResource
from transplants.frontend.resources.solution_resource import SolutionResource
from transplants.frontend.resources.solver_config_resource import SolverConfigResource

app = Flask(__name__)

api = Api(app)

api.add_resource(ProblemResource, "/problem/<string:problem_id>")
api.add_resource(SolverConfigResource, "/solver_config/<string:solver_config_id>")
api.add_resource(SolutionResource, "/solution/<string:solution_id>")
api.add_resource(JobResource, "/job/<string:job_id>")
api.add_resource(JobsResource, "/jobs/")
api.add_resource(PatientResource, "/patient/<string:patient_id>")

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

docs.register(ProblemResource)
docs.register(SolverConfigResource)
docs.register(SolutionResource)
docs.register(JobResource)
docs.register(JobsResource)
docs.register(PatientResource)


def start_app(database: Database, host: str = "localhost", port: int = 5000, debug: bool = True):
    setup_db(database=database, clean=True)
    start_job_processing()
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    start_app(database=kidney_exchange_database)
