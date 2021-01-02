from typing import Dict, List

from transplants.core.patient.medical_data.hla_system.hla_antibody import HLAAntibody
from transplants.core.patient.patient import Patient
from transplants.core.patient.serialize_to_dict.hla_system import code_to_antigen
from transplants.core.scorer.hla_blood_type_additive_scorer import HLABloodTypeAdditiveScorer
from transplants.core.scorer.scorer_base import TRANSPLANT_IMPOSSIBLE
from transplants.core.solution.transplant import Transplant


def scorer_from_params(scorer_parameters: Dict, patients: List[Patient], add_related_to_forbidden: bool = True):
    """API utility function that creates Scorer according to the specified parameters

    Args:
        scorer_parameters: parameter specification
        patients: patients -- used for resolving the actual patients from their identifiers in the scorer_parameters
            argument
        add_related_to_forbidden: add (related donor, recipient) pairs if the recipient is not looking for a better
            donor than he already has

    Returns:
        Scorer object that assigns {-inf, float} value to Matching (in special cases also to Chains and Transplants)
    """
    forbidden_transplants = list(scorer_parameters.get("forbidden_transplants", []))
    if add_related_to_forbidden:
        additional_forbidden_transplants = [(donor.identifier, patient.identifier)
                                            for patient in patients
                                            if patient.is_recipient and not patient.require_better_than_related_match
                                            for donor in patient.related_donors]
        forbidden_transplants.extend(additional_forbidden_transplants)

    scorer_type = scorer_parameters["type"]
    code_to_patient = {patient.identifier: patient for patient in patients}

    compatible_blood_group_bonus = scorer_parameters.get("compatible_blood_group_bonus", 10.0)
    incompatible_blood_group_malus = scorer_parameters.get("incompatible_blood_group_malus", TRANSPLANT_IMPOSSIBLE)
    hla_allele_compatibility_bonus = scorer_parameters.get("hla_allele_compatibility_bonus", None)
    max_allowed_antibody_concentration = {
        HLAAntibody(code_to_antigen.get(antibody_code)): concentration for antibody_code, concentration
        in scorer_parameters.get("max_allowed_antibody_concentration", dict()).items()
    }
    forbidden_transplants = [Transplant(donor=code_to_patient[donor_code], recipient=code_to_patient[recipient_code])
                             for donor_code, recipient_code in forbidden_transplants]
    min_required_base_score = float(scorer_parameters.get("min_required_base_score", 0.0))
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
