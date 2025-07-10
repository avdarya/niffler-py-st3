### Тестовые данные для пользователя заполняются в .env файле

### Шаги
1. Склонировать проект
```bash
   git clone https://github.com/avdarya/niffler-py-st3.git
```
2. Добавить файл .env (см файл .env_sample). Поля заполнить данными для созданной заранее учетной записи 
3. Перейти в корневой каталог проекта
```bash
  cd niffler-py-st3
```
4. Запустить микросервис
```bash
  docker-compose-dev.sh
```
5. Запустить тесты:
Из корневого каталога проекта
```bash
  chmod +x run_tests.sh
  ./run_tests.sh
  ./run_tests.sh --env=rc
```
Из директории с тестами
```bash
  pytest --env=rc 
```



#!/bin/bash

set -e

export PYTHONPATH=$(pwd)/niffler_tests

echo "Running all tests..."
pytest niffler_tests_python "$@"

