test: lint unit-test acceptance-test
all: clean test build

POETRY = poetry

clean:
	@echo "---- Doing cleanup ----"
	@rm -rf .mypy_cache .pytest_cache dist

install:
	@echo "---- Installing package ---- "
	@$(POETRY) install

lint:
	@echo "---- Running type check and linter ---- "
	@$(POETRY) run mypy napi

unit-test:
	@echo "---- Running unit tests ---- "
	@$(POETRY) run pytest -ra -vv test/unit

acceptance-test:
	@echo "---- Running acceptance tests ---- "
	@$(POETRY) run pytest -ra -vv test/acceptance

build:
	@echo "---- Build distributable ---- "
	@$(POETRY) build

.PHONY: all config test build clean setup install lint ut at
