from typing import Set


class BloodType:
    _VALID_ANTIGEN_ANTIBODY_CODES = ["0", "A", "B", "AB"]

    def __init__(self, antigen_codes: Set[str], antibody_codes: Set[str]):
        self._antigen_codes = tuple(sorted(antigen_codes))
        self._antibody_codes = tuple(sorted(antibody_codes))
        self._validate()

    def __hash__(self):
        return hash(tuple([self._antigen_codes, self._antibody_codes]))

    def __eq__(self, other):
        if not isinstance(other, BloodType):
            return False

        return self._antigen_codes == other._antigen_codes and \
               self._antibody_codes == other._antibody_codes

    def __str__(self) -> str:
        return self.code

    def __repr__(self) -> str:
        return self.code

    @property
    def code(self) -> str:
        return "".join(sorted(self._antigen_codes)) or "0"

    def can_give_to(self, blood_group: "BloodType") -> bool:
        for code in self._antigen_codes:
            if code in blood_group._antibody_codes:
                return False
        return True

    def can_receive_from(self, blood_group: "BloodType") -> bool:
        return blood_group.can_give_to(self)

    def _validate(self):
        for code in self._antigen_codes + self._antibody_codes:
            if code not in BloodType._VALID_ANTIGEN_ANTIBODY_CODES:
                raise AssertionError(f"Invalid code {self._code}")


BloodType.ZERO = BloodType(antigen_codes={}, antibody_codes={"A", "B"})
BloodType.A = BloodType(antigen_codes={"A"}, antibody_codes={"B"})
BloodType.B = BloodType(antigen_codes={"B"}, antibody_codes={"A"})
BloodType.AB = BloodType(antigen_codes={"A", "B"}, antibody_codes={})

BloodType.O = BloodType.ZERO  # 0 is not valid name, but O is
BloodType.ALL = [BloodType.ZERO, BloodType.A, BloodType.B, BloodType.AB]

if __name__ == '__main__':
    def display(flag) -> str:
        return "o" if flag else "x"


    title = "Compatibility table donor (column) -> recipient (row)"
    print(title)
    print("-" * len(title))
    print(" \t" + "\t".join(list(map(str, BloodType.ALL))))
    for blood_type_recipient in BloodType.ALL:
        transplant_ok = [display(blood_type_donor.can_give_to(blood_type_recipient))
                         for blood_type_donor in BloodType.ALL]
        transplant_ok = str(blood_type_recipient) + "\t" + "\t".join(transplant_ok)
        print(transplant_ok)
