🪙 Niffler Autotests (Python Advanced)

Проект создан в рамках курса
«Автоматизация тестирования для продвинутых инженеров (Python Advanced)»
https://qa.guru/python-advanced￼

Автотесты разработаны для тестирования учебного микросервисного приложения Niffler (кошелёк), включающего UI, REST API, SOAP, Kafka, GraphQL и gRPC взаимодействия.

🎯 Цели проекта
	•	Автоматизировать тестирование всех уровней приложения Niffler.
	•	Обеспечить удобный запуск тестов как локально, так и в Docker-контейнере.
	•	Организовать параллельное выполнение тестов и формирование Allure-отчёта.
	•	Реализовать CI-pipeline в GitHub Actions.

🧩 Использованные технологии
	•	Python 3.12, Poetry, Pytest, Playwright
	•	Allure для отчётности
	•	Pydantic для типизации моделей данных
	•	Kafka-Python и psycopg2 / SQLAlchemy для работы с Kafka и PostgreSQL
	•	gRPC, GraphQL, SOAP — интеграционные проверки
	•	Pytest-xdist — параллельный запуск тестов
	•	Docker, Docker Compose — окружение для тестов
	•	GitHub Actions — CI/CD

🧪 Типы реализованных тестов
Тип тестов
Описание
UI тесты
Проверка основных пользовательских сценариев кошелька (создание, редактирование, удаление трат, регистрация, логин).
REST API тесты
Проверка CRUD-операций микросервисов auth, spend, category.
SOAP тесты
Проверка SOAP-методов сервиса userdata.
Kafka тесты
Проверка публикации и консумирования сообщений после регистрации пользователей.
GraphQL тесты
Проверка корректности запросов stat, user, spend через GraphQL API.
gRPC тесты
Проверка методов CalculateRate и GetAllCurrencies сервиса NifflerCurrencyService.
DB тесты
Проверка корректности записей в PostgreSQL после действий пользователей.

⚙️ Установка проекта
1. Подготовка окружения
```bash
    git clone https://github.com/avdarya/niffler-py-st3.git
    cd niffler-py-st3-avdarya/niffler_tests_python
    poetry install
    source $(poetry env info --path)/bin/activate
    cp .env_sample .env 
```
2. Запуск микросервисов
```bash
    bash ../docker-compose-dev.sh 
```
Локальный запуск тестов
4. 
5. Запуск тестов
```bash
    pytest
```
🌐 UI-тесты в браузере Chrome (по умолчанию)
```bash
    pytest tests/ui
```
🌐 UI-тесты в Firefox
```bash
    pytest --browser=firefox tests/ui
```
⚡ Параллельный запуск
```bash
    pytest -n auto
```
📊 Формирование Allure-отчёта
```bash
    pytest --alluredir=allure-results
    allure serve allure-results
```

🐳 Запуск тестов в Docker-контейнере




### Шаги
1. Склонировать проект
```bash
   git clone https://github.com/avdarya/niffler-py-st3.git
```

2. Перейти в корневой каталог проекта
```bash
    cd niffler-py-st3-avdarya
```
3. Запустить микросервис
```bash
    bash docker-compose-dev.sh
```
4. Добавить файл .env (см файл .env_sample). Поля username, password заполнить данными для созданной заранее учетной записи
```bash
    cp .env_sample .env
```
5. Перейти в дирректорию с тестами
```bash
  cd niffler_tests_python
```
6. Установить зависимости проекта
```bash
    poetry install
```
7. Получить путь к виртуальному окружению
```bash
    poetry env info --path 
```
Пример вывода
```bash
   путь_до_виртуального_окружения
```
8. Запустить виртуальное окружение
```bash
    source путь_до_окружения/bin/activate
```
9. Запустить тесты:
- API + UI тесты
```bash
    pytest 
```
- UI тесты в выбранном браузере: chrome (выбран по умолчанию), firefox
```bash
    pytest --browser=firefox tests/ui
```
- API тесты
```bash
    pytest tests/api 
```
10. Просмотреть allure-отчет
```bash 
    allure serve
```

grpc curl
```bash
     grpcurl -plaintext localhost:8092 list
```

```bash
    grpcurl -plaintext localhost:8092 list guru.qa.grpc.niffler.NifflerCurrencyService
```
guru.qa.grpc.niffler.NifflerCurrencyService.CalculateRate
guru.qa.grpc.niffler.NifflerCurrencyService.GetAllCurrencies


описание метода CalculateRate
```bash
    grpcurl -plaintext localhost:8092 describe guru.qa.grpc.niffler.NifflerCurrencyService.CalculateRate
```
```bash
    grpcurl -plaintext localhost:8092 describe guru.qa.grpc.niffler.CalculateRequest
```
вызвать метод
```bash
    grpcurl -plaintext \
      -d '{"spendCurrency": 2, "desiredCurrency": 1, "amount": 1}' \
      localhost:8092 guru.qa.grpc.niffler.NifflerCurrencyService.CalculateRate
```
```bash
    grpcurl -plaintext localhost:8092 describe guru.qa.grpc.niffler.NifflerCurrencyService.GetAllCurrencies
```
```bash
    grpcurl -plaintext \
    localhost:8092 guru.qa.grpc.niffler.NifflerCurrencyService.GetAllCurrencies
```
генерация протобафов
```bash
    pbreflect get-protos -h localhost:8092 -o ./tests/grpc/protos
```
```bash
    pbreflect generate --proto-dir ./protos --output-dir ./generated --gen-type pbreflect
```

старт контейнера currencymock
```bash
    docker compose -f docker-compose.grpcmock.yml up
```
