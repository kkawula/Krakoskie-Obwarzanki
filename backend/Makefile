.ONESHELL:

.DEFAULT_GOAL := server

PYTHON = ./venv/bin/python3
PIP = ./venv/bin/pip


venv/bin/activate: requirements.txt requirements-dev.txt
	python -m venv venv
	chmod +x venv/bin/activate
	. ./venv/bin/activate
	$(PIP) install -r requirements.txt
	$(PIP) install -r requirements-dev.txt
#  -r requirements-dev.txt
# pre-commit install
# make pre-commit-install


venv: venv/bin/activate
	. ./venv/bin/activate

# Run the server
server: venv
	python app/main.py

clean:
	find . -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf venv

pre-commit-install: .pre-commit-config.yaml
	pre-commit install


.PHONY: pre-commit-run pre-commit-all-files clean server

# Run pre-commit on all files in staging area
pre-commit-run: pre-commit-install
	pre-commit run

# Run pre-commit on all files
pre-commit-all-files: pre-commit-install
	pre-commit run --all-files
