.PHONY: clean experiment lint requirements test venv

#################################################################################
# GLOBALS                                                                       #
#################################################################################
VENV_DIR =  env
PYTHON_INTERPRETER = $(VENV_DIR)/bin/python3
PIP = $(VENV_DIR)/bin/pip

#################################################################################
# COMMANDS                                                                      #
#################################################################################
all: clean requirements lint test


## Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Run experiments
experiment:
	@$(PYTHON_INTERPRETER) ./src/marketsim/experiments/*.py

## Lint using flake8
lint:
	@$(PYTHON_INTERPRETER) -m flake8 --max-line-length=90 ./src/marketsim ./test

## Run tests
test:
	@$(PYTHON_INTERPRETER) -W ignore::DeprecationWarning -m unittest discover --verbose

## Install Python Dependencies
requirements: venv
	$(PIP) install -U pip setuptools wheel
	$(PIP) install -e .
ifneq ($(wildcard ./requirements.txt),)
	$(PIP) install -r requirements.txt
endif


## Install virtual environment
venv:
ifeq ($(wildcard $(VENV_DIR)/*),)
	@echo "Did not find $(VENV_DIR), creating..."
	mkdir -p $(VENV_DIR)
	python3 -m venv $(VENV_DIR)
endif

