from logging import exception
from threading import Thread
from typing import Dict

from transplants.utils.find_exchanges import find_exchanges
from web.utils.solution_store import SolutionStore


def _token_from_exchange_params(exchange_parameters: Dict) -> str:
    """Injective function from exchange parameters to string"""
    # TODO: Implement
    pass


def _solve_and_dump_to_db(exchange_parameters: Dict, token: str, solution_store: SolutionStore):
    try:
        exchanges = find_exchanges(exchange_parameters=exchange_parameters)
        solution_store.dump_solution(token=token, solution=exchanges)
    except:
        exception(f"Finding exchanges failed")
        solution_store.mark_incomplete(token=token)


def solve_async(exchange_parameters: Dict, solution_store: SolutionStore) -> str:
    """Asynchronously run transplants.utils.find_exchnages on the exchange parameters and when the result is ready
    save it in database under the token id which is derived from the exchanged parameters and returned
    """
    token = _token_from_exchange_params(exchange_parameters)
    if not solution_store.solution_exists():
        solution_store.dump_solution(token=token, solution=None)
        thread = Thread(
            target=_solve_and_dump_to_db, kwargs=dict(
                exchange_parameters=exchange_parameters,
                token=token,
                solution_store=solution_store
            )
        )
        thread.start()
    return token
