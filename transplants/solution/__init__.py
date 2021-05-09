from transplants.solution.chain import Chain
from transplants.solution.cycle import Cycle
from transplants.solution.sequence import Sequence

Chain.is_cycle_to_constructor[True] = Cycle
Chain.is_cycle_to_constructor[False] = Sequence
