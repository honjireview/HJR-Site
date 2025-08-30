#!/bin/sh

# Устанавливаем права на исполнение, на всякий случай
chmod +x /app/start.sh

echo "--- Запускаем Gunicorn (ваше Flask приложение) в фоновом режиме ---"
# Запускаем Gunicorn в фоновом режиме на внутреннем порту 8000
gunicorn --bind 0.0.0.0:8000 app:app &

echo "--- Создаем конфигурацию Nginx на основе шаблона ---"
# Подставляем системную переменную $PORT в наш шаблон
envsubst '$PORT' < /app/nginx.conf.template > /etc/nginx/conf.d/default.conf

echo "--- Запускаем Nginx в основном режиме ---"
# Запускаем Nginx, который теперь будет проксировать запросы к Gunicorn
nginx -g 'daemon off;'