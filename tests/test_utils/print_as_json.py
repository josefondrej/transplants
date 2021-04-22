import json

from tests.test_utils.load_job import load_job
from tests.test_utils.load_problem import load_problem
from tests.test_utils.load_solver_config import load_solver_config


def print_json(obj):
    print(json.dumps(obj.to_dict()))


if __name__ == '__main__':
    print_json(load_problem())
    print_json(load_solver_config())
    print_json(load_job())
