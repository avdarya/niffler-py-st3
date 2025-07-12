### Шаги
1. Склонировать проект
```bash
   git clone https://github.com/avdarya/niffler-py-st3.git
```
2. Добавить файл .env (см файл .env_sample). Поля username, password заполнить данными для созданной заранее учетной записи 
3. Перейти в корневой каталог проекта
```bash
    cd niffler-py-st3
```
4. Запустить микросервис
```bash
    docker-compose-dev.sh
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