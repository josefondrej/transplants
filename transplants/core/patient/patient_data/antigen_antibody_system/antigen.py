class Antigen:
    """Generic class for antigen."""

    def __init__(self, code: str):
        self._code = code

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        else:
            return self.code == other.code

    def __hash__(self):
        return hash(self.code)

    def __str__(self):
        return self.code

    def __repr__(self):
        return self.code

    @property
    def code(self) -> str:
        return self._code
