config: venv-clean venv install
all: test build

PY3 = python3
VENV = .venv/napi.py
VENV_PY3 = .venv/napi.py/bin/python3

venv-clean:
	@echo "---- Doing cleanup ----"
	@mkdir -p .venv
	@rm -rf $(VENV)

venv:
	@echo "---- Setting virtualenv ----"
	@$(PY3) -m venv $(VENV)
	@echo "---- Installing dependencies and app itself in editable mode ----"
	@$(VENV_PY3) -m pip install --upgrade pip

install:
	@$(VENV_PY3) -m pip install -e .[dev]

test:
	@echo "---- Testing ---- "
	@$(VENV_PY3) -m mypy --ignore-missing-imports ./napi
	@$(VENV_PY3) -m pytest -v ./test

build:
	@echo "---- Building package ---- "
	@$(VENV_PY3) setup.py sdist bdist_wheel --python-tag py3 --dist-dir ./dist

.PHONY: all config test build
