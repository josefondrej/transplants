from typing import Dict

from transplants.patient.medical_data.hla_system.hla_antibody import HLAAntibody
from transplants.scorer.hla_blood_type_additive_scorer import HLABloodTypeAdditiveScorer
from transplants.scorer.scorer_base import TRANSPLANT_IMPOSSIBLE
from transplants.serialization.hla_system import code_to_antigen


def from_dict(dictionary: Dict):
    scorer_type = dictionary["type"]

    if scorer_type == "HLABloodTypeAdditiveScorer":
        max_allowed_antibody_concentration = {
            HLAAntibody(code_to_antigen.get(antibody_code)): concentration for antibody_code, concentration
            in dictionary.get("max_allowed_antibody_concentration", dict()).items()
        }

        scorer = HLABloodTypeAdditiveScorer(
            compatible_blood_group_bonus=dictionary.get("compatible_blood_group_bonus", 10.0),
            incompatible_blood_group_malus=dictionary.get("incompatible_blood_group_malus", TRANSPLANT_IMPOSSIBLE),
            hla_allele_compatibility_bonus=dictionary.get("hla_allele_compatibility_bonus", None),
            max_allowed_antibody_concentration=max_allowed_antibody_concentration,
            forbidden_transplants=list(dictionary.get("forbidden_transplants")),
            min_required_base_score=float(dictionary.get("min_required_base_score", 0.0))
        )
        return scorer
    else:
        raise ValueError(f"Invalid solver type {scorer_type} provided")
