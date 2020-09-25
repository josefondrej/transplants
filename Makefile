include .env.pub

conda-create:
	conda env create -f conda.yml --name $(CONDA_ENV)

conda-export:
	conda env export --from-history

conda-update:
	conda env update --file conda.yml --prune --name $(CONDA_ENV)

conda-activate:
	conda activate $(CONDA_ENV)
