### Тестовые данные для пользователя заполняются в .env файле

### Шаги
1. Склонировать проект
```bash
   git clone https:    /python-advanced-intro-4.git
```
2. Установить зависимости
```bash
    pip install -r requirements.txt
```
3. Запустить микросервис "Запуск Niffler в докере":
```bash
bash docker-compose-dev.sh
```
4. Запустить тесты:
```bash
  pytest --env=rc 
```
