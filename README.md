# Проект “Табло теннисного матча” 
Веб-приложение, реализующее табло счёта теннисного матча.
https://zhukovsd.github.io/python-backend-learning-course/projects/tennis-scoreboard/
## О проекте
### Технологии

- Python 3.12 - коллекции, ООП
- Паттерн MVC(S)
- pip/Poetry
- Backend
  - uWSGI, wsgiref
  - Веб - GET и POST запросы, формы
  - Jinja2
- Базы данных - MySQL, SQLAlchemy
- Frontend - HTML/CSS, блочная вёрстка
- Тесты - юнит тестирование
- Деплой - облачный хостинг, командная строка Linux

### Мотивация проекта

- Создать клиент-серверное приложение с веб-интерфейсом
- Получить практический опыт работы с ORM SQLAlchemy и инструментом миграций Alembic
- Сверстать простой веб-интерфейс без сторонних библиотек
- Познакомиться с архитектурным паттерном MVC(S)

### Подсчёт очков в теннисном матче

В теннисе особая система подсчёта очков - https://www.gotennis.ru/read/world_of_tennis/pravila.html

Для упрощения, допустим что каждый матч играется по следующим правилам:

- Матч играется до двух сетов (best of 3)
- При счёте 6/6 в сете, играется тай-брейк до 7 очков

# Использование
### Установка
```shell
git clone https://github.com/mandalorianec/TennisMatchScoreboard.git
cd TennisMatchScoreboard\tennis_match_scoreboard
```
### Создание базы данных

Инструкция по созданию и настройки базы данных MySQL

## Устновка MySQL

1) Скачать MySQL Installer
2) Установить MySQL Community Server, задать root-пароль и запомнить его
3) в powershell ввести это(создание базы данных и пользователя). Подставить root-пароль после -p. Вместо login/pwd
   подставить свои значения

```shell
mysql -u root -p -e "CREATE DATABASE db CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci; CREATE USER 'login'@'localhost' IDENTIFIED BY 'pwd'; GRANT ALL PRIVILEGES ON db.* TO 'login'@'localhost'; FLUSH PRIVILEGES;"   
```

4) Создайте и настройте .env в корне проекта: tennis_match_scoreboard/.env. Можно сделать бд более гибкой, используя
   закомментированные переменные. Для простоты оставил только необходимые.

```
USERNAME_DB=login
PASSWORD_DB=pwd
; DB_HOST=localhost
; DB_NAME=db
; DB_DRIVER=mysql+pymysql
DISABLE_LOGGING=false
```

5) Если библиотеки ещё не установлены:

```shell
poetry install
poetry env activate
```

6) Применить миграции

```shell
alembic -c alembic.ini upgrade head
```

7) запустить файл **main.py**

### Запуск тестов
из директории проекта: \tennis_match_scoreboard>
```shell
python -m unittest discover -s tests -p "test_*.py" -v
```
