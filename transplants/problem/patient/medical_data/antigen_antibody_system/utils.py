from transplants.problem.patient.medical_data.antigen_antibody_system.antibody import Antibody
from transplants.problem.patient.medical_data.antigen_antibody_system.antigen import Antigen
from transplants.problem.patient.medical_data.blood_type_system.blood_type_antibody import BloodTypeAntibody
from transplants.problem.patient.medical_data.blood_type_system.blood_type_antigen import BloodTypeAntigen
from transplants.problem.patient.medical_data.hla_system.hla_antibody import HLAAntibody
from transplants.problem.patient.medical_data.hla_system.hla_antigen import HLAAntigen

_antigen_class_to_antibody_class = {
    Antigen: Antibody,
    BloodTypeAntigen: BloodTypeAntibody,
    HLAAntigen: HLAAntibody
}


def anti(antigen: Antigen) -> Antibody:
    constructor = _antigen_class_to_antibody_class.get(antigen.__class__, Antibody)
    return constructor(antigen)
