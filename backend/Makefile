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
	make install-dev

install: requirements.txt
	$(PIP) install -r requirements.txt

install-dev: requirements-dev.txt
	$(PIP) install -r requirements-dev.txt
	make pre-commit-install

pre-commit-install: .pre-commit-config.yaml
	pre-commit install

# SERVER
.PHONY: server
# Run the server
server: venv/bin/activate
	. ./venv/bin/activate
	$(PYTHON) app/main.py

.PHONY: pre-commit-run
# Run pre-commit on all files in staging area
pre-commit-run: pre-commit-install
	pre-commit run

.PHONY: pre-commit-all-files
# Run pre-commit on all files
pre-commit-all-files: pre-commit-install
	pre-commit run --all-files

.PHONY: clean
clean:
	find . -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf venv
