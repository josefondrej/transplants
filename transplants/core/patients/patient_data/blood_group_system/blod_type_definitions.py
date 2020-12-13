import transplants.core.patients.patient_data.blood_group_system.blood_type_antigen_definitions as blood_antigen
from transplants.core.patients.patient_data.antigen_antibody_system.utils import anti
from transplants.core.patients.patient_data.blood_group_system.blood_type import BloodType

ZERO = BloodType(antigens={}, antibodies={anti(blood_antigen.A), anti(blood_antigen.B)})
O = ZERO
A = BloodType(antigens={blood_antigen.A}, antibodies={anti(blood_antigen.B)})
B = BloodType(antigens={blood_antigen.B}, antibodies={anti(blood_antigen.A)})
AB = BloodType(antigens={blood_antigen.A, blood_antigen.B}, antibodies={})

all_types = [ZERO, A, B, AB]

if __name__ == '__main__':
    def _bool_to_symbol(value: bool) -> str:
        return "o" if value else "x"


    print("Donor -> Recipient Compatibility Table")
    print("-" * 38)
    print("\t" + "\t".join([str(blood_type) for blood_type in all_types]))
    for blood_type_donor in all_types:
        row = str(blood_type_donor) + "\t" + "\t".join(
            [_bool_to_symbol(blood_type_donor.can_give_to(blood_type_recipient)) for blood_type_recipient in all_types])
        print(row)
