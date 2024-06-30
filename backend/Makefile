.ONESHELL:

.DEFAULT_GOAL := server

PYTHON = ./venv/bin/python3
PIP = ./venv/bin/pip

# INSTALLATIONS
venv/bin/activate: requirements.txt requirements-dev.txt
	python3 -m venv venv
	chmod +x venv/bin/activate
	. ./venv/bin/activate
	make install

install: requirements.txt
	$(PIP) install -r requirements.txt --no-cache-dir

dev: requirements-dev.txt .pre-commit-config.yaml
	$(PIP) install -r requirements-dev.txt --no-cache-dir
	pre-commit install

# SERVER
.PHONY: server
# Run the server
server: venv/bin/activate
	. ./venv/bin/activate
	$(PYTHON) app/main.py

test: venv/bin/activate
	. ./venv/bin/activate
	$(PYTHON) -m pytest

.PHONY: pre-commit
# Run pre-commit on all files in staging area
pre-commit:
	pre-commit run

.PHONY: pre-commit-all
# Run pre-commit on all files
pre-commit-all:
	pre-commit run --all-files

.PHONY: clean
clean:
	find . -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf venv
