include .env.pub

conda-create:
	conda create --name $(CONDA_ENV) --file requirements.txt

requirements-export:
	pigar

conda-activate:
	conda activate $(CONDA_ENV)

run-tests:
	bash ./run_tests.sh

run-web-api:
	bash ./run_web_api.sh