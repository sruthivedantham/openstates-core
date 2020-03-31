#!/bin/sh
set -e
export PYTHONPATH=.; poetry run pytest --cov openstates_core --cov-report html --ds=openstates_core.test_settings --cov-config=.coveragerc $@
coverage report -m
