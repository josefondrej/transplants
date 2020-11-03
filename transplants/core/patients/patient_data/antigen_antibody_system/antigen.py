from dataclasses import dataclass


@dataclass(frozen=True)
class Antigen:
    """Generic class for antigen."""
    code: str

    def __str__(self):
        return self.code
