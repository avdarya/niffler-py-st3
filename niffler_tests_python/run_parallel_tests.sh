#!/usr/bin/env bash
set -e

pytest -m isolated --clean-alluredir --alluredir=allure-results/isolated
pytest -m "not isolated" -n auto --alluredir=allure-results/not_isolated

allure generate allure-results/isolated allure-results/not_isolated -o allure-report --clean
allure open allure-report