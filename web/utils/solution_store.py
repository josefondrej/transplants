import os
from datetime import datetime
from logging import exception
from plistlib import Dict
from typing import List, Optional

from pymongo import MongoClient


class SolutionWrapper:
    allowed_status = ["in_progress", "failed", "ready", "archived"]
    datetime_format = "%d/%m/%y %H:%M:%S"

    def __init__(self, token: str, status: str, last_modified: datetime, payload: Dict = None):
        if status not in SolutionWrapper.allowed_status:
            raise ValueError(f"Invalid status {status}")

        self._token = token
        self._status = status
        self._last_modified = last_modified
        self._payload = payload

    def to_dict(self) -> Dict:
        serialized_solution = {
            "token": self._token,
            "status": self._status,
            "last_modified": self._last_modified.strftime(fmt=SolutionWrapper.datetime_format),
            "payload": self._payload
        }

        return serialized_solution

    @classmethod
    def from_dict(cls, dictionary: Dict) -> "SolutionWrapper":
        solution_wrapper = SolutionWrapper(
            token=dictionary["token"],
            status=dictionary["status"],
            last_modified=datetime.strptime(date_string=dictionary["last_modified"],
                                            format=SolutionWrapper.datetime_format),
            payload=dictionary["payload"]
        )

        return solution_wrapper


class SolutionStore:
    DATABASE_NAME = "transplants"
    COLLECTION_NAME = "solutions"

    def __init__(self):
        connection_credentials = self._load_credentials_from_env()
        self._client = MongoClient(**connection_credentials)
        self._database = self._client[SolutionStore.DATABASE_NAME]
        self._collection = self._database.get_collection(SolutionStore.COLLECTION_NAME)

    def dump_solution(self, solution: SolutionWrapper) -> bool:
        try:
            self._collection.insert_one(document=solution.to_dict())
            return True
        except:
            exception("Dumping solution failed")
            return False

    def get_solution(self, token: str) -> Optional[SolutionWrapper]:
        solution = self._collection.find_one(filter=self._filter_from_token(token))
        return solution

    def solution_exists(self, token: str) -> bool:
        solution = self._collection.find_one(
            filter=self._filter_from_token(token),
            projection={}
        )

        solution_exists = (solution is not None)
        return solution_exists

    def get_status(self, token: str) -> str:
        solution = self._collection.find_one(
            filter=self._filter_from_token(token),
            projection={"status": True}
        )

        solution_status = solution["status"]
        return solution_status

    def get_all_solutions(self) -> List[SolutionWrapper]:
        solutions = self._collection.find(projection={"token": True, "status": True, "last_modified": True})
        return [SolutionWrapper.from_dict(dictionary) for dictionary in solutions]

    def _load_credentials_from_env(self) -> Dict:
        # TODO: Add password
        host = os.getenv("MONGO_HOST")
        port = os.getenv("MONGO_PORT")
        return {"host": host, "port": port}

    def _filter_from_token(self, token: str) -> Dict:
        return {"token": token}
