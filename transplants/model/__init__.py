from transplants.model.chain import Chain
from transplants.model.cycle import Cycle
from transplants.model.donor import Donor
from transplants.model.patient import Patient
from transplants.model.patient_type import PatientType
from transplants.model.recipient import Recipient
from transplants.model.sequence import Sequence

Chain.is_cycle_to_constructor[True] = Cycle
Chain.is_cycle_to_constructor[False] = Sequence

Patient.type_to_constructor[PatientType.RECIPIENT.value] = Recipient
Patient.type_to_constructor[PatientType.DONOR.value] = Donor
