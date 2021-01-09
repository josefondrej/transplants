from flask import Flask
from flask_restful import Api

from transplants.web_api.endpoints.job import Job
from transplants.web_api.endpoints.jobs import Jobs

app = Flask(__name__)

api = Api(app)

api.add_resource(Job, "/job/<string:token>")
api.add_resource(Jobs, "/jobs")

if __name__ == '__main__':
    app.run(port=5000, debug=True)
