config: clean setup install
all: test build

PY3 = python3
VENV = .venv/$(basename $PWD)
VENV_PY3 = .venv/$(basename $PWD)/bin/python3

clean:
	@echo "---- Doing cleanup ----"
	@rm -rf .venv .tox .mypy_cache *.egg-info build dist
	@mkdir -p .venv

setup:
	@echo "---- Setting virtualenv ----"
	@$(PY3) -m venv $(VENV)
	@echo "---- Installing dependencies and app itself in editable mode ----"
	@$(VENV_PY3) -m pip install --upgrade pip

install:
	@$(VENV_PY3) -m pip install -e .[dev]

test:
	@echo "---- Testing ---- "
	@$(VENV_PY3) -m tox

build:
	@echo "---- Building package ---- "
	@$(VENV_PY3) setup.py sdist bdist_wheel --python-tag py3 --dist-dir ./dist

publish:
	@echo "---- Publishing package ---- "


.PHONY: all config test build
