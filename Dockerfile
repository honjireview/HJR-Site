# Используем официальный образ Nginx
FROM nginx:alpine

# Устанавливаем gettext для утилиты envsubst, которая нужна для подстановки порта
RUN apk update && apk add gettext

# Копируем ваш HTML файл
COPY index.html /usr/share/nginx/html

# Копируем шаблон конфигурации Nginx
COPY nginx.conf.template /etc/nginx/templates/

# Копируем и делаем исполняемым скрипт запуска
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Команда для запуска нашего скрипта при старте контейнера
CMD ["/start.sh"]