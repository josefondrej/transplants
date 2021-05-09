from typing import Dict, List, Optional, Tuple

from transplants.backend.scorer.additive_scorer_base import AdditiveScorerBase
from transplants.backend.scorer.scorer_base import TRANSPLANT_IMPOSSIBLE
from transplants.model.medical_data.blood_type_system.blood_type import BloodType
from transplants.model.medical_data.hla_system.antigen_definitions import A_antigens, B_antigens, \
    DRB1_antigens
from transplants.model.medical_data.hla_system.hla_antibody import HLAAntibody
from transplants.model.medical_data.hla_system.hla_system import HLASystem
from transplants.model.problem import Problem
from transplants.model.transplant import Transplant


class HLABloodTypeAdditiveScorer(AdditiveScorerBase):
    """Basic scorer that considers compatibility in the blood groups and HLA system

    Args:
        compatible_blood_group_bonus: Bonus for donor & recipient having compatible blood groups
        incompatible_blood_group_malus: Malus for donor & recipient having incompatible blood groups,
            set either to TRANSPLANT_IMPOSSIBLE or to 0.0 to forbid or allow transplant across blood group
        hla_allele_compatibility_bonus: Dictionary of {gene_code: bonus for match in one allele of that gene
            between donor and recipient}. Each gene can match in 0, 1 or 2 alleles -- so the bonus for one allele
            gets multiplied accordingly
        max_allowed_antibody_concentration: If recipient has lower than this concentration of the particular antibody
            then we do not consider it as reason for positive crossmatch
    """

    def __init__(
            self,
            compatible_blood_group_bonus: float = 10.0,
            incompatible_blood_group_malus: float = TRANSPLANT_IMPOSSIBLE,
            hla_allele_compatibility_bonus: Optional[Dict[str, float]] = None,
            max_allowed_antibody_concentration: Optional[Dict[HLAAntibody, float]] = None,
            forbidden_transplants: Optional[List[Tuple[str, str]]] = None,
            min_required_base_score: float = 0.0
    ):
        self._compatible_blood_group_bonus = compatible_blood_group_bonus
        self._incompatible_blood_group_malus = incompatible_blood_group_malus
        self._hla_allele_compatibility_bonus = hla_allele_compatibility_bonus or {"A": 1.0, "B": 3.0, "DRB1": 9.0}
        self._max_allowed_antibody_concentration = max_allowed_antibody_concentration or {}
        super().__init__(forbidden_transplants=forbidden_transplants,
                         min_required_base_score=min_required_base_score)

    def score_transplant_base(self, transplant: Transplant, problem: Problem) -> float:
        donor = problem.get_patient(transplant.donor_id)
        recipient = problem.get_patient(transplant.recipient_id)

        transplant_score = 0.0

        transplant_score += self._blood_type_compatibility_score(
            donor_blood_type=donor.medical_data.blood_type,
            recipient_blood_type=recipient.medical_data.blood_type
        )

        transplant_score += self._hla_compatibility_score(
            donor_hla_system=donor.medical_data.hla_system,
            recipient_hla_system=recipient.medical_data.hla_system
        )

        return transplant_score

    def _blood_type_compatibility_score(self, donor_blood_type: BloodType, recipient_blood_type: BloodType) -> float:
        if donor_blood_type.can_give_to(recipient_blood_type):
            return self._compatible_blood_group_bonus
        else:
            return self._incompatible_blood_group_malus

    def _hla_compatibility_score(self, donor_hla_system: HLASystem, recipient_hla_system: HLASystem) -> float:
        virtual_hla_crossmatch_is_positive = self._hla_crossmatch_is_positive(
            donor_hla_system=donor_hla_system,
            recipient_hla_system=recipient_hla_system
        )
        if virtual_hla_crossmatch_is_positive:
            return TRANSPLANT_IMPOSSIBLE

        match_in_antigens_score = self._hla_match_in_antigens_score(
            donor_hla_system=donor_hla_system,
            recipient_hla_system=recipient_hla_system
        )
        return match_in_antigens_score

    def _hla_crossmatch_is_positive(self, donor_hla_system: HLASystem, recipient_hla_system: HLASystem) -> bool:
        # TODO: Implement functionality for dealing with broads & splits
        # TODO: Implement functionality for considering antibody concentrations lower
        #  than self._max_allowed_antibody_concentration
        return recipient_hla_system.has_antibodies_for(donor_hla_system.antigens)

    def _hla_match_in_antigens_score(self, donor_hla_system: HLASystem, recipient_hla_system: HLASystem) -> float:
        score = 0.0
        for gene_name, gene_compatibility_bonus in self._hla_allele_compatibility_bonus.items():
            common_count = self._count_common_alleles(
                gene_name=gene_name,
                donor_hla_system=donor_hla_system,
                recipient_hla_system=recipient_hla_system
            )
            score += common_count * gene_compatibility_bonus

        return score

    def _count_common_alleles(self, gene_name: str, donor_hla_system: HLASystem,
                              recipient_hla_system: HLASystem) -> int:
        """Counts the number of common alleles of specified gene

        Args:
            gene_name: Name of gene for which to count the common alleles (e.g. A, B, DRB1)
            donor_hla_system: HLA system of donor
            recipient_hla_system: HLA system of recipient

        Returns: Count of common antigens, can be 0 / 1 / 2
        """
        donor_allele_codes, recipient_allele_codes = [self._get_allele_list(gene_name=gene_name, hla_system=hla_system)
                                                      for hla_system in [donor_hla_system, recipient_hla_system]]
        common_allele_count = 0

        for donor_allele_code in donor_allele_codes:
            common_allele_count += recipient_allele_codes.count(donor_allele_code)

        return common_allele_count

    def _get_allele_list(self, gene_name: str, hla_system: HLASystem) -> List[str]:
        """Get list (of length = 2) of alleles corresponding to the gene name from the HLA system

        Since we only have the data on serologically defined antigens in the HLASystem, we do not return the actual
        alleles but just codes of the broad antigens, which should be good enough for our purposes
        """
        antigens = self._get_antigens_coded_by_gene(gene_name=gene_name, hla_system=hla_system)
        allele_codes = {antigen.broad.code if antigen.broad is not None else antigen.code for antigen in antigens}
        allele_codes = list(allele_codes) * 2 if len(allele_codes) == 1 else list(allele_codes)

        if len(allele_codes) != 2:
            raise AssertionError(f"Invalid number of alleles: {allele_codes}")

        return allele_codes

    def _get_antigens_coded_by_gene(self, gene_name: str, hla_system: HLASystem):
        gene_name_to_antigens = {
            "A": A_antigens,
            "B": B_antigens,
            "DRB1": DRB1_antigens
        }

        if gene_name not in gene_name_to_antigens:
            raise NotImplementedError(f"Not implemented for gene {gene_name}")

        all_antigens_coded_by_gene = gene_name_to_antigens[gene_name]
        antigens_coded_by_gene = {antigen for antigen in hla_system.antigens
                                  if antigen in all_antigens_coded_by_gene}
        return antigens_coded_by_gene
