#!/bin/bash

set -e

export PYTHONPATH=$(pwd)/niffler_tests

echo "Running all tests..."
pytest niffler_tests "$@"