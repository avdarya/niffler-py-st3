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
