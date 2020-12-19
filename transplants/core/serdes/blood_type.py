from copy import deepcopy
from typing import Dict

from transplants.core.patient.medical_data.blood_group_system.blod_type_definitions import all_types
from transplants.core.patient.medical_data.blood_group_system.blood_type import BloodType

_str_to_blood_type = {str(bt): bt for bt in all_types}


def to_dict(blood_type: BloodType) -> Dict:
    dictionary = {
        "type": str(blood_type),
        "forbidden_types": list(map(str, blood_type.forbidden_blood_types))
        if blood_type.forbidden_blood_types is not None else None
    }

    return dictionary


def from_dict(dictionary: Dict) -> BloodType:
    blood_type = deepcopy(_str_to_blood_type[dictionary["type"]])
    if dictionary.get("forbidden_types") is not None:
        blood_type._forbidden_blood_types = [_str_to_blood_type[bt] for bt in dictionary["forbidden_types"]]

    return blood_type
