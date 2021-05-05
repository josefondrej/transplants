from transplants.problem.patient.donor import Donor
from transplants.problem.patient.patient import Patient
from transplants.problem.patient.patient_type import PatientType
from transplants.problem.patient.recipient import Recipient

Patient.type_to_constructor[PatientType.RECIPIENT.value] = Recipient
Patient.type_to_constructor[PatientType.DONOR.value] = Donor
