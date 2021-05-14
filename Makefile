include .env.pub

conda-create:
	conda create --name $(CONDA_ENV) --file requirements.txt

requirements-export:
	pigar

conda-activate:
	conda activate $(CONDA_ENV)

run-solve-api-test:
	bash ./run_solve_api.sh kidney_exchange_test

run-tests:
	bash ./run_tests.sh

run-solve-api:
	bash ./run_solve_api.sh