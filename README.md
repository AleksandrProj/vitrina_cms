# CMS для партнерских проектов

## Инструкция по установке
### Локальная установка
1. Делаем файл .env из .env.example (cp .env.example .env)
2. Меняем данные в .env файле на свои
3. Запускаем команду "docker compose -f docker/docker-compose.yaml up -d --build"

## Замечания по Операционным системам
### Linux/Ubuntu
- При работе на Linux/Ubuntu необходимо на папки которые монтируются через volume ставить права 777
- makemigrations запускаем основном терминале, а migrate в терминале самого docker контейнера

## Инструменты
* Python - программный код
* Poetry - менеджер пакетов Python
* Django/Wagtail - CMS сайта
* PostgreSQL - База данных для сайта
* Docker - контейнеризация для сайта
* Nginx - Веб-сервер для сайта