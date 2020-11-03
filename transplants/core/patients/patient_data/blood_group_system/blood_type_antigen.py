from transplants.core.patients.patient_data.antigen_antibody_system.antigen import Antigen


class BloodTypeAntigen(Antigen):
    pass


BloodTypeAntigen.A = BloodTypeAntigen(code="A")
BloodTypeAntigen.B = BloodTypeAntigen(code="B")
