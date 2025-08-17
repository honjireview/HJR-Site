#!/bin/sh

# Подставляем значение переменной PORT в шаблон и создаем рабочий конфиг
envsubst '$PORT' < /etc/nginx/templates/nginx.conf.template > /etc/nginx/conf.d/default.conf

# Запускаем Nginx в режиме, который не позволяет контейнеру завершиться
nginx -g 'daemon off;'