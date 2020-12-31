from typing import Dict, List

from transplants.core.patient.medical_data.hla_system.hla_antibody import HLAAntibody
from transplants.core.patient.patient import Patient
from transplants.core.patient.serialize_to_dict.hla_system import code_to_antigen
from transplants.core.scorer.hla_blood_type_additive_scorer import HLABloodTypeAdditiveScorer
from transplants.core.scorer.scorer_base import TRANSPLANT_IMPOSSIBLE
from transplants.core.solution.transplant import Transplant


def scorer_from_params(params: Dict, patients: List[Patient]):
    scorer_type = params["type"]
    code_to_patient = {patient.identifier: patient for patient in patients}

    compatible_blood_group_bonus = params.get("compatible_blood_group_bonus", 10.0)
    incompatible_blood_group_malus = params.get("incompatible_blood_group_malus", TRANSPLANT_IMPOSSIBLE)
    hla_allele_compatibility_bonus = params.get("hla_allele_compatibility_bonus", None)
    max_allowed_antibody_concentration = {HLAAntibody(code_to_antigen.get(antibody_code)): concentration for
                                          antibody_code, concentration
                                          in params.get("max_allowed_antibody_concentration", dict())}
    forbidden_transplants = [Transplant(donor=code_to_patient[donor_code], recipient=code_to_patient[recipient_code])
                             for donor_code, recipient_code in params.get("forbidden_transplants", [])]
    min_required_base_score = float(params.get("min_required_base_score", 0.0))
    if scorer_type == "HLABloodTypeAdditiveScorer":
        scorer = HLABloodTypeAdditiveScorer(
            compatible_blood_group_bonus=compatible_blood_group_bonus,
            incompatible_blood_group_malus=incompatible_blood_group_malus,
            hla_allele_compatibility_bonus=hla_allele_compatibility_bonus,
            max_allowed_antibody_concentration=max_allowed_antibody_concentration,
            forbidden_transplants=forbidden_transplants,
            min_required_base_score=min_required_base_score
        )
        return scorer
    else:
        raise ValueError(f"Invalid solver type {scorer_type} provided")