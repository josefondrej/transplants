from transplants.core.patient.patient import Patient


class Donor(Patient):
    @property
    def is_donor(self) -> bool:
        return True

    @property
    def is_recipient(self) -> bool:
        return False
