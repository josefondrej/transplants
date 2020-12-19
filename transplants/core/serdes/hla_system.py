from typing import Dict

from transplants.core.patient.medical_data.hla_system.antigen_definitions import all_antigens
from transplants.core.patient.medical_data.hla_system.hla_antibody import HLAAntibody
from transplants.core.patient.medical_data.hla_system.hla_system import HLASystem

_str_to_antigen = {antigen.code: antigen for antigen in all_antigens}


def to_dict(hla_system: HLASystem) -> Dict:
    dictionary = {
        "antigens": {antigen.code for antigen in hla_system.antigens},
        "antibodies": {antibody.code: concentration for antibody, concentration in
                       hla_system.antibody_to_concentration.items()}
    }

    return dictionary


def from_dict(dictionary: Dict) -> HLASystem:
    antigens = {_str_to_antigen.get(code) for code in dictionary["antigens"]
                if code in _str_to_antigen}
    antibodies = {HLAAntibody(_str_to_antigen.get(code)): concentration
                  for code, concentration in dictionary["antibodies"].items()
                  if code in _str_to_antigen}

    hla_system = HLASystem(
        antigens=antigens,
        antibodies=antibodies
    )

    return hla_system
