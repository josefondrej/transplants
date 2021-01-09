from flask import request
from flask_restful import Resource


class Job(Resource):
    """TODO: Implement
    job = {
        "token": "abc",
        "status": "in_progress",
        "problem_description": {...},
        "problem_solution": None
    }
    """
    new_token = "new"

    def get(self, token: str):
        """Get job by token"""
        # TODO: Implement
        if token == Job.new_token:
            return {"message": "Wrong method GET for submitting a new job"}, 400

        job = Job(token=token)

        return {"token": token}

    def post(self, token: str):
        """Submit new job for solving"""
        # TODO: Implement
        if token != Job.new_token:
            return {"message": "Wrong method POST for retrieving an existing job"}, 400

        problem_description = request.json
        return {"token": "123", "problem_description": problem_description}
