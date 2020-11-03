from transplants.core.patients.patient_data.antigen_antibody_system.antibody import Antibody
from transplants.core.patients.patient_data.blood_group_system.blood_type_antigen import BloodTypeAntigen


class BloodTypeAntibody(Antibody):
    pass


BloodTypeAntibody.A = BloodTypeAntibody(antigen=BloodTypeAntigen.A)
BloodTypeAntibody.B = BloodTypeAntibody(antigen=BloodTypeAntigen.B)
