from typing import Optional, Dict, Any, Union, List


class SolverConfig:
    def __init__(self, solver_config_id: str, solver_name: str, parameters: Optional[Dict] = None):
        self._solver_config_id = solver_config_id
        self._solver_name = solver_name
        self._parameters = parameters

    def __eq__(self, other):
        if not isinstance(other, SolverConfig):
            return False

        return (self.solver_config_id == other.solver_config_id) and (self.solver_name == other.solver_name) \
               and (self.parameters == other.parameters)

    def __hash__(self):
        return hash((self.solver_config_id, self.solver_name, frozenset(self.parameters)))

    @property
    def solver_config_id(self) -> str:
        return self._solver_config_id

    @property
    def solver_name(self):
        return self._solver_name

    @property
    def parameters(self) -> Dict:
        return self._parameters

    def add_parameter(self, name: str, value: Any, force_update: bool = False):
        if name in self._parameters and not force_update:
            raise KeyError(f"Key {name} already present in parameters, use with force_update=True to override")
        self._parameters[name] = value

    def append_values_to_list_parameter(self, name: str, values: Union[Any, List[Any]]):
        if name not in self._parameters:
            self._parameters[name] = list()

        if not isinstance(values, list):
            values = [values]

        self._parameters[name].extend(values)
