from typing import Dict, Set, Union

from transplants.patient.medical_data.antigen_antibody_system.antigen_antibody_system import AntigenAntibodySystem
from transplants.patient.medical_data.blood_type_system.blood_type_antibody import BloodTypeAntibody
from transplants.patient.medical_data.blood_type_system.blood_type_antigen import BloodTypeAntigen


class BloodType(AntigenAntibodySystem):
    """Blood type of patient

    Args:
        antigens: Set of antigens
        antibodies: Set of antibodies
        forbidden_blood_types: Set of blood types of donors from who the patient can't receive transplant even
            if we allow transplants across blood type
    """

    def __init__(self, antigens: Set[BloodTypeAntigen],
                 antibodies: Union[Set[BloodTypeAntibody], Dict[BloodTypeAntibody, float]],
                 forbidden_blood_types: Set["BloodType"] = None):
        super().__init__(antigens=antigens, antibodies=antibodies)
        self._forbidden_blood_types = forbidden_blood_types

    def can_give_to(self, recipient_blood_type: "BloodType") -> bool:
        """Can patient with this blood type give blood to patient with recipient_blood_type"""
        return not recipient_blood_type.has_antibodies_for(self.antigens)

    def can_receive_from(self, donor_blood_type: "BloodType") -> bool:
        """Can patient with this blood type receive blood from patient with donor_blood_type"""
        return donor_blood_type.can_give_to(self)

    def __str__(self) -> str:
        representation = "".join(sorted(map(str, self.antigens)))
        return "0" if len(representation) == 0 else representation

    @property
    def forbidden_blood_types(self) -> Set["BloodType"]:
        return self._forbidden_blood_types
