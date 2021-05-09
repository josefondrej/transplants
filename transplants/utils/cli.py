import argparse

from transplants.database.mongo_db import kidney_exchange_database
from transplants.database.purge_db import purge_db
from transplants.utils.load_donors_recipients import load_donors_recipients_from_file
from transplants.utils.paths import get_abs_path
from transplants.utils.print_blood_type_compatibility_table import print_blood_type_compatibility_table
from transplants.utils.visualise_problem import visualise_test_problem

parser = argparse.ArgumentParser(description="Transplants Command Line Interface")
parser.add_argument("--purge-db", required=False, help="Purge database")
parser.add_argument("--show-test-patients", required=False, help="Show test patients")
parser.add_argument("--print-blood-type-compatibility-table", required=False,
                    help="Prints blood type compatibility table")
parser.add_argument("--visualise-test-problem", required=False, help="Visualise test model")

args = parser.parse_args()

if args.purge_db is not None:
    print("Purging database ...")
    purge_db(kidney_exchange_database)

if args.show_test_patients is not None:
    test_donors, test_recipients = load_donors_recipients_from_file(
        get_abs_path("./tests/test_utils/patient_pool_example.json"))
    test_patients = test_donors + test_recipients

    for test_patient in test_patients:
        serialized_patient = test_patient.to_dict()
        print(serialized_patient)

if args.print_blood_type_compatibility_table is not None:
    print_blood_type_compatibility_table()

if args.visualise_test_problem is not None:
    visualise_test_problem()
