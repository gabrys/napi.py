#!/usr/bin/env bash

set -e

if [ "$TRAVIS_BRANCH" == "master" ]; then
    echo "Uploading as user: $PYPI_USER"
    twine upload -u $PYPI_USER -p $PYPI_PASSWORD dist/*
  else
    echo "Not on CI master branch, not publishing"
fi