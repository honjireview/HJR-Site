# Используем официальный образ Nginx
FROM nginx:alpine

# Копируем ваш HTML файл в директорию, где Nginx хранит сайты
COPY index.html /usr/share/nginx/html

# Указываем, что контейнер будет слушать порт 80
EXPOSE 80

# Команда для запуска Nginx при старте контейнера
CMD ["nginx", "-g", "daemon off;"]