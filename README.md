# GameHub

Игровая образовательная платформа.

## Деплой

### Установка ПО

    apt-get install git, python-dev, python-pip, redis-server
    curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -
    sudo apt-get install -y nodejs

    git clone git@gitlab.com:zdimon77/gamehub.git
    ./bin/install

## Запуск вэб сервера разработки

    ./bin/webserver


## Запуск сокет сервера.

    ./bin/socketserver

## Запуск селери.    

    ./bin/celery

[Техническая документация](docs/Home.md)
