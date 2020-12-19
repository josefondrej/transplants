from transplants.core.patient.patient_type import PatientType

_str_to_patient_type = {patient_type.value: patient_type for patient_type in PatientType}


def to_str(patient_type: PatientType) -> str:
    return patient_type.value


def from_str(string: str) -> PatientType:
    patient_type = _str_to_patient_type[string]
    return patient_type
