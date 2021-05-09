from abc import ABC, abstractmethod

from transplants.model.problem import Problem
from transplants.model.solution import Solution
from transplants.model.solver_config import SolverConfig


class SolverBase(ABC):
    """Base class for backend

    Defines the basic solve(Problem) -> Solution interface
    """

    @abstractmethod
    def solve(self, problem: Problem) -> Solution:
        """Return list of scored matchings sorted by their .score if available"""
        pass

    @classmethod
    def build_from_config(cls, config: SolverConfig) -> "SolverBase":
        """Factory method that creates Solver from SolverConfig"""
        pass
