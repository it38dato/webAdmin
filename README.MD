# Информационный портал базовых станций (Nokia / Ericsson) 

Task: 
Необходимо установить и настроить веб-сервер «Информационный портал», в котором отображается информация о базовых станциях Nokia и Ericsson. 
Decision: 
Веб-сервер изначально разрабатывается для тестовой среды Windows с использованием Django и автоматизации через BAT-скрипты. Для работы необходимо: Python 3.10, Django, Виртуальное окружение, База данных (SQLite3 / MySQL / PostgresSQL)
Примечания:
1. Проект предназначен для тестовой и боевой среды
2. Поддерживается Windows и Linux
3. Основной стек: Python / Django / MySQL

Task: 
Установка и настройка (Windows / Linux) 
Decision: 
1. Установка Python: Скачать и установить Python 3.10, убедиться, что он добавлен в PATH. 
2. Проверка Python: Запустить checkPython.bat, для Линукс систем - checkPython.sh. 
Скрипты проверяют наличие Python в системе.
3. Создание Django-проекта: Запустить checkDjango.bat, для Линукс систем - checkDjango.sh.
Что делает скрипт: Создаёт виртуальное окружение, Устанавливает зависимости из requirements.txt, Создаёт Django-проект в домашней директории, Запрашивает Имя виртуального окружения (SET VENV_NAME=...), Название проекта, Логин и пароль администратора и Показывает Команду активации виртуального окружения и Путь к исходным файлам проекта.
Файл requirements.txt должен находиться в той же папке, откуда запускается checkDjango.bat.
4. Запуск тестового сервера: Запустить Скрипт startDjango.bat, для Линукс систем - startDjango.sh. 
Скрипт запрашивает Название проекта, IP-адрес. Если IP не указан, используется: http://127.0.0.1:8000
Если в settings.py изменён параметр:
ALLOWED_HOSTS = []
необходимо указать IP и порт, прописанные в ALLOWED\_HOSTS (например: 127.0.0.1:8000)
Остановка сервера - CTRL + C

Task: 
Готовые проекты
Decision: 
В папке projects/ находятся готовые версии веб-сервера.
Перед запуском готового проекта необходимо:
- Изменить параметры в settings.py: ALLOWED\_HOSTS, INSTALLED\_APPS, TEMPLATES, DATABASES, customColorPalette, CKEDITOR\_5\_CONFIGS
- Скопировать и заменить файлы: webAdminTemplate/urls.py, webPages/\*.html, webApp/\*.py, config.json
- Запустить startDjango.bat, для Линукс систем - startDjango.sh.
- Ввести параметры из config.json

Task: 
Работа с базами данных. По умолчанию используется SQLite3. 
Decision: 
1. Посмотреть данные в SQLite3 можно командами:
sudo apt install sqlite3
sqlite3 db.sqlite3
.tables
.q
2. Для Импорта данных из Excel в SQLite3 есть скрипт ImportExcelSqlite.py
3. Создание БД MySQL (продакшн):
CREATE DATABASE your_database_name CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
4. Настройка settings.py:
DATABASES = { 'default': { 'ENGINE': 'mysql.connector.django', 'NAME': 'your_database_name', 'USER': 'your_user', 'PASSWORD': 'your_password', 'HOST': 'localhost', 'PORT': '3306', 'OPTIONS': { 'init_command': "SET sql_mode='STRICT_TRANS_TABLES'", 'charset': 'utf8mb4', 'use_unicode': True, } } }
5. Миграция данных из SQLite в MySQL Экспорт данных: importDjangoSql1.bat
6. Миграция данных из SQLite в MySQL Импорт в MySQL: importDjangoSql2.bat
7. Создание БД PSQL (продакшн):
Скрипт checkPsql.sh проверяют наличие БД в системе.
Команды для настройки БД:
sudo -u postgres psql
\password postgres
CREATE DATABASE sqlite3;
CREATE USER myuser WITH PASSWORD 'testPassword';
GRANT ALL PRIVILEGES ON DATABASE sqlite3 TO myuser;
\q
Настройка /etc/postgresql/14/main/pg_hba.conf:
host    all             all             0.0.0.0/0               md5
Настройка /etc/postgresql/16/main/postgresql.conf: 
listen_addresses = '\*'
sudo systemctl restart postgresql
sudo ufw allow 5432/tcp
psql -U dato -d sqlite3 -h localhost

Task: 
Миграция проекта (Linux)
Decision:
1. Для переноса Django-проекта с Windows на Linux используется migrateDjango.sh. 
2. executeFile.sh предоставляет права на исполнение файла.
3. Проверка сервиса:
sudo systemctl status bss_portal.service

Task:
Админ-панель Django
Decision:
1. Создание суперпользователя:
python3 manage.py createsuperuser
Для Windows можно использовать 
migrateDjango.bat

Task:
GitHub публикация проекта
Decision:
для публикации проекта после внесения изменений можно использовать скрипт pushGithub.sh

Task:
Тестовые проекты
Decision:
Папка testImportKeys:
1. testLibrary.py использует библиотеку importKeys.py
2. Данные подтягиваются из config.txt
3. Для веб-портала не используется, т.к. применяется config.json и другая логика.