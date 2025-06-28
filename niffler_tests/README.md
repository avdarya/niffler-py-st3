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
```bash
  chmod +x run_tests.sh
  ./run_tests.sh
  ./run_tests.sh --env=rc
  pytest --env=rc 
```