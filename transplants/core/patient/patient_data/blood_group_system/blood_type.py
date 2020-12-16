from transplants.core.patient.patient_data.antigen_antibody_system.antigen_antibody_system import AntigenAntibodySystem


class BloodType(AntigenAntibodySystem):
    def can_give_to(self, recipient_blood_type: "BloodType") -> bool:
        return not recipient_blood_type.has_antibodies_for(self.antigens)

    def can_receive_from(self, donor_blood_type: "BloodType") -> bool:
        return donor_blood_type.can_give_to(self)

    def __str__(self) -> str:
        representation = "".join(sorted(map(str, self.antigens)))
        return "0" if len(representation) == 0 else representation
