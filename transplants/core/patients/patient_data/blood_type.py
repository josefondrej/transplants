from typing import Set

VALID_CODES = ["0", "A", "B", "AB"]


class BloodType:
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
        return "".join(self._antigen_codes) or "0"

    def can_give_to(self, blood_group: "BloodType") -> bool:
        for code in self._antigen_codes:
            if code in blood_group._antibody_codes:
                return False
        return True

    def can_receive_from(self, blood_group: "BloodType") -> bool:
        return blood_group.can_give_to(self)

    def _validate(self):
        for code in self._antigen_codes + self._antibody_codes:
            if code not in VALID_CODES:
                raise AssertionError(f"Invalid code {self._code}")


BT_0 = BloodType(antigen_codes={}, antibody_codes={"A", "B"})
BT_A = BloodType(antigen_codes={"A"}, antibody_codes={"B"})
BT_B = BloodType(antigen_codes={"B"}, antibody_codes={"A"})
BT_AB = BloodType(antigen_codes={"A", "B"}, antibody_codes={})

BLOOD_TYPES = [BT_0, BT_A, BT_B, BT_AB]

code_to_blood_type = dict(zip(VALID_CODES, BLOOD_TYPES))
blood_type_to_code = dict(zip(BLOOD_TYPES, VALID_CODES))

if __name__ == '__main__':
    def display(flag) -> str:
        return "o" if flag else "x"


    print("Compatibility table donor (column) -> recipient (row)")
    print("-" * 70)
    print(" \t" + "\t".join(list(map(str, BLOOD_TYPES))))
    for blood_type_recipient in BLOOD_TYPES:
        transplant_ok = [display(blood_type_donor.can_give_to(blood_type_recipient))
                         for blood_type_donor in BLOOD_TYPES]
        transplant_ok = str(blood_type_recipient) + "\t" + "\t".join(transplant_ok)
        print(transplant_ok)
