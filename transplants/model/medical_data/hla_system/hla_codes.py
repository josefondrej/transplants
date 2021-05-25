from transplants.model.medical_data.hla_system.antigen_definitions import B_antigens, A_antigens, DRB1_antigens, \
    all_antigens

other_antigens = set(all_antigens) - set(A_antigens) - set(B_antigens) - set(DRB1_antigens)

hla_code_groups = [
    ("hla_a", A_antigens),
    ("hla_b", B_antigens),
    ("hla_drb1", DRB1_antigens),
    ("other", other_antigens)
]

hla_code_groups = [(grp_name, [str(antigen) for antigen in antigen_list]) for grp_name, antigen_list in
                   hla_code_groups]
all_hla_codes = [str(antigen) for antigen in all_antigens]
