.ONESHELL:

.DEFAULT_GOAL := server

PYTHON = ./venv/bin/python3
PIP = ./venv/bin/pip

# INSTALLATIONS

venv/bin/activate: requirements.txt requirements-dev.txt
	python -m venv venv
	chmod +x venv/bin/activate
	. ./venv/bin/activate
	$(PIP) install -r requirements.txt
	$(PIP) install -r requirements-dev.txt
#  -r requirements-dev.txt
# pre-commit install
	make pre-commit-install

pre-commit-install: .pre-commit-config.yaml
	pre-commit install


.PHONY: server
# Run the server
server: venv/bin/activate
	. ./venv/bin/activate
	python app/main.py

.PHONY: clean
clean:
	find . -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf venv




.PHONY: pre-commit-run
# Run pre-commit on all files in staging area
pre-commit-run: pre-commit-install
	pre-commit run

.PHONY: pre-commit-all-files
# Run pre-commit on all files
pre-commit-all-files: pre-commit-install
	pre-commit run --all-files
