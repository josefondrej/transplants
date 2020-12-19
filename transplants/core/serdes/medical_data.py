from typing import Dict

from transplants.core.patient.medical_data.medical_data import MedicalData
from transplants.core.serdes.blood_type import to_dict as blood_type_to_dict, from_dict as blood_type_from_dict
from transplants.core.serdes.hla_system import to_dict as hla_system_to_dict, from_dict as hla_system_from_dict


def to_dict(medical_data: MedicalData) -> Dict:
    dictionary = {
        "blood_type": blood_type_to_dict(medical_data.blood_type),
        "hla_system": hla_system_to_dict(medical_data.hla_system)
    }

    return dictionary


def from_dict(dictionary: Dict) -> MedicalData:
    medical_data = MedicalData(
        blood_type=blood_type_from_dict(dictionary["blood_type"]),
        hla_system=hla_system_from_dict(dictionary["hla_system"])
    )

    return medical_data
