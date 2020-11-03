from transplants.core.patients.patient_data.antigen_antibody_system.antigen_antibody_system import AntigenAntibodySystem
from transplants.core.patients.patient_data.blood_group_system.blood_type_antibody import BloodTypeAntibody
from transplants.core.patients.patient_data.blood_group_system.blood_type_antigen import BloodTypeAntigen


class BloodType(AntigenAntibodySystem):
    def can_give_to(self, recipient_blood_type: "BloodType") -> bool:
        return not recipient_blood_type.has_antibodies_for(self.antigens)

    def can_receive_from(self, donor_blood_type: "BloodType") -> bool:
        return donor_blood_type.can_give_to(self)

    def __str__(self) -> str:
        representation = "".join(sorted(map(str, self.antigens)))
        return "0" if len(representation) == 0 else representation


BloodType.ZERO = BloodType(antigens={}, antibodies={BloodTypeAntibody.A, BloodTypeAntibody.B})
BloodType.A = BloodType(antigens={BloodTypeAntigen.A}, antibodies={BloodTypeAntibody.B})
BloodType.B = BloodType(antigens={BloodTypeAntigen.B}, antibodies={BloodTypeAntibody.A})
BloodType.AB = BloodType(antigens={BloodTypeAntigen.A, BloodTypeAntigen.B}, antibodies={})

BloodType.ALL = [BloodType.ZERO, BloodType.A, BloodType.B, BloodType.AB]
BloodType.O = BloodType.ZERO

if __name__ == '__main__':
    def _bool_to_symbol(value: bool) -> str:
        return "o" if value else "x"


    print("Donor -> Recipient Compatibility Table")
    print("-" * 38)
    print("\t" + "\t".join([str(blood_type) for blood_type in BloodType.ALL]))
    for blood_type_donor in BloodType.ALL:
        row = str(blood_type_donor) + "\t" + "\t".join(
            [_bool_to_symbol(blood_type_donor.can_give_to(blood_type_recipient))
             for blood_type_recipient in BloodType.ALL])
        print(row)
