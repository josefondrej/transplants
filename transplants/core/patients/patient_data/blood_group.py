class BloodGroup:
    def __init__(self, code: str):
        self._code = code

    def __hash__(self):
        return hash(self._code)

    def __eq__(self, other):
        if not isinstance(other, BloodGroup):
            return False

        return self._code == other._code
