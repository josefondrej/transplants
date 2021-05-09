from enum import Enum


class PatientType(Enum):
    DONOR = "donor"
    RECIPIENT = "recipient"

    def __str__(self):
        return self.value
