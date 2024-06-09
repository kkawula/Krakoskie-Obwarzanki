# Target: venv
# Description: Creates a virtual environment and installs dependencies.
venv: venv/touchfile

# Target: venv/touchfile
# Description: Checks if the virtual environment exists, creates it if not, and installs dependencies.
# Run `make venv prod=true` to install only production dependencies.
venv/touchfile: requirements.txt requirements-dev.txt
	test -d venv || python3 -m venv venv
	. venv/bin/activate;
	make install
	if [ -z "$(prod)" ]; then\
        make install-dev;\
        make pre-commit-install;\
    fi
	touch venv/touchfile

# Install dependencies
install:
	pip install -r requirements.txt

# Install development dependencies
install-dev:
	pip install -r requirements-dev.txt
pre-commit-install:
	pre-commit install

# Run the server
server:
	python app/main.py

.PHONY: pre-commit-run pre-commit-all-files clean

# Run pre-commit on all files in staging area
pre-commit-run:
	pre-commit run

# Run pre-commit on all files
pre-commit-all-files:
	pre-commit run --all-files

clean:
	rm -rf venv
	find -iname "*.pyc" -delete
