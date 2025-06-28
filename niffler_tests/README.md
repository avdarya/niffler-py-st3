### Тестовые данные для пользователя заполняются в .env файле

### Шаги
1. Склонировать проект
```bash
   git clone https://github.com/avdarya/niffler-py-st3.git
```
3. Перейти в корневой каталог проекта
```bash
  cd niffler-py-st3
```
4. Запустить микросервис
```bash
  docker-compose-dev.sh
```
4. Запустить тесты:
```bash
  pytest --env=rc 
```
