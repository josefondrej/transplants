import copy
from typing import Dict, Set, Union

from marshmallow import fields
from marshmallow.validate import OneOf

from transplants.model.medical_data.antigen_antibody_system.antigen_antibody_system import \
    AntigenAntibodySystem
from transplants.model.medical_data.antigen_antibody_system.utils import anti
from transplants.model.medical_data.blood_type_system import blood_type_antigen_definitions as blood_antigen
from transplants.model.medical_data.blood_type_system.blood_type_antibody import BloodTypeAntibody
from transplants.model.medical_data.blood_type_system.blood_type_antigen import BloodTypeAntigen
from transplants.model.medical_data.blood_type_system.blood_type_codes import AB_code, B_code, A_code, \
    ZERO_code, all_blood_type_codes
from transplants.serialization.serialization_mixin import SerializationMixin, add_marshmallow_schema, \
    serializable_property

_blood_type_code_validator = OneOf([blood_type_code for blood_type_code in all_blood_type_codes])


@add_marshmallow_schema
class BloodType(AntigenAntibodySystem, SerializationMixin):
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

    @serializable_property(fields.List(fields.String(validate=_blood_type_code_validator), allow_none=True),
                           serialize_name="forbidden_types")
    def forbidden_blood_types(self) -> Set["BloodType"]:
        return self._forbidden_blood_types

    @serializable_property(fields.String())
    def type(self):
        return str(self)

    @classmethod
    def _marshmallow_post_load(cls, data):
        code = data["type"]
        forbidden_codes = data["forbidden_blood_types"]
        model = copy.deepcopy(code_to_blood_type[code])
        model._forbidden_blood_types = None if forbidden_codes is None \
            else [code_to_blood_type[code] for code in forbidden_codes]
        return model


ZERO = BloodType(antigens=set(), antibodies={anti(blood_antigen.A), anti(blood_antigen.B)})
A = BloodType(antigens={blood_antigen.A}, antibodies={anti(blood_antigen.B)})
B = BloodType(antigens={blood_antigen.B}, antibodies={anti(blood_antigen.A)})
AB = BloodType(antigens={blood_antigen.A, blood_antigen.B}, antibodies=set())
all_types = [ZERO, A, B, AB]
code_to_blood_type = {ZERO_code: ZERO, A_code: A, B_code: B, AB_code: AB}
