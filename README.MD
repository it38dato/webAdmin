Task:
необоходимо установить и настроить веб сервер "Информационны портал", в котором будет отображаться вся информация о базовых станциях Nokia и Ercisson
Decision:
Веб-сервер изначально будет работать для тестовой версии в Windows. Поэтому для настройки сервера использую скрипты bat. 
Необходимо скачать Python (У меня 3.10) и установить ее. Затем использовать скрипты:
- checkPython.bat для проверки Python
- checkDjango.bat для настройки переменного окружения и создания проекта Django. Скрипт checkDjango.bat установит в домашнюю директорию переменную окружения. В строке:
SET VENV_NAME=...
можно перед запуском скрипта добавить свое название. Скрипт запросит название проекта и данный проект будет находиться в домашней директории, покажет какой командой звпускать переменную окруженния и куда установил исходные файлы веб-сервера и запрашивает логин и пароль для регистрации админ панели.
- startDjango.bat - используется для тестового запуска веб-сервера. Для начального тестового старта можно запустить скрипт startDjango.bat. скрипт также запросит имя проекта, которое дали в скрипте checkPython.bat и Ip адрес, в котором установлен проект. Можно ip адрес не заполнять если проект тестовый, так как адрес по умолчанию будет настроен http://127.0.0.1:8000. если в файле settings.py поменяли параметры:
ALLOWED_HOSTS = []
тогда в скрипте startDjango.bat при запросе ip адреса нужно добавить свой ip с портом взятый из файла settings.py в ALLOWED_HOSTS (например: 127.0.0.1:8000). Командой CTRL-c можно первать работу веб-сервера.
В папке projects есть готовые проекты веб-сервера. Для запуска проекта необходимо Поменять данные (библиотеки, ALLOWED_HOSTS, INSTALLED_APPS, TEMPLATES, DATABASES, customColorPalette, CKEDITOR_5_CONFIGS) в файле Settings.py, скопировать и переместить в проект с заменой webAdminTemplate/urls.py, webPages/*.html, webApp/*.py, config.json. Запустить скрипт startDjango.bat и ввести данные из ваших параметров config.json. 
В файле requirements.txt библиотеки для работы с проектом. файл должен находиться в той же папке, в которой вы звпускаете скрипт checkDjango.bat.
при необхохдимсти работы с Sqlite3 файл ImportExcelSqlite.py добавляет в Sqlite3 информацию из excel.
По умолчанию используется БД sqlite3. у нас же используется Mysql. Поэтому необходимо провести миграцию данных с Sqlite3 в Mysql. командой создал Базу данных в mysql:
CREATE DATABASE your_database_name CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
в папке importDjangoSql скриптом importDjangoSql1.bat записал данные в json, внес изменения в Settings
    DATABASES = {
        'default': {
            'ENGINE': 'mysql.connector.django',
            'NAME': 'your_database_name',
            'USER': 'your_user',     # Имя пользователя MySQL
            'PASSWORD': 'your_password', # Пароль пользователя MySQL
            'HOST': 'localhost',     # Хост (обычно localhost или 127.0.0.1)
            'PORT': '3306',
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",            
                'charset': 'utf8mb4', 
                'use_unicode': True,
            }
        }
    }
и скриптом importDjangoSql2.bat импортировал данные с Sqlite3 в Mysql.
Так как я переносил тестовый веб-сервер Django с Windows на боевую виртуальную Linux миграцию проекта Django выполнил скриптом bash migrateDjango.sh. Перед выполнением скрипта необходимо дать права на исполнение файла и выполнить скрипт командами:
sudo chmod +X migrateDjango.sh
./migrateDjango.sh
sudo systemctl status bss_portal.service
Для того чтобы дать доступ к Админ панели необхоимдо дать команду:
python3 manage.py createsuperuser
в Windows можно запустить скрипт migrateDjango.bat. Тоже делает миграцию в Django.
Есть папка с проектом testImportKeys. файл testLibrary.py использует библиотеку файла importKeys.py и подтягивает данные из файла config.txt. Для проекта веб сервера это не актуально, так как используется config.json и другая функция.

