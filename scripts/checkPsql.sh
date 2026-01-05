#!/bin/bash

# Функция для определения пакетного менеджера
install_logic() {
    if [ -f /etc/debian_version ]; then
        echo "Обновление кэша и установка PostgreSQL (Debian/Ubuntu)..."
        sudo apt-get update
        # Устанавливаем именно серверный пакет
        sudo apt-get install -y postgresql postgresql-contrib
    elif [ -f /etc/redhat-release ]; then
        echo "Установка PostgreSQL (RHEL/CentOS)..."
        sudo yum install -y postgresql-server postgresql-contrib
        sudo postgresql-setup initdb || echo "База уже инициализирована"
        sudo systemctl enable postgresql
    else
        echo "ОС не поддерживается скриптом."
        exit 1
    fi
}

echo "=== Проверка PostgreSQL ==="

# 1. Проверяем, установлен ли именно сервер (наличие службы)
if ! systemctl list-unit-files | grep -q "postgresql.service"; then
    echo "Сервер PostgreSQL не найден (отсутствует служба)."
    install_logic
else
    echo "Сервер PostgreSQL установлен."
fi

# 2. Проверка и запуск службы
echo "--- Статус службы ---"
if systemctl is-active --quiet postgresql; then
    echo "Служба PostgreSQL уже запущена."
else
    echo "Служба не активна. Попытка запуска..."
    sudo systemctl start postgresql
    
    # Проверка после попытки запуска
    if systemctl is-active --quiet postgresql; then
        echo "Служба успешно запущена."
    else
        echo "Ошибка: Не удалось запустить PostgreSQL. Проверьте логи: journalctl -xeu postgresql"
        exit 1
    fi
fi

# 3. Вывод версии
echo "--- Информация о версии ---"
psql --version

# 4. Проверка готовности принимать соединения
echo "--- Проверка готовности БД ---"
sudo -u postgres pg_isready
