# Используем легковесный официальный образ веб-сервера Nginx
FROM nginx:1.25-alpine

# Удаляем стандартную конфигурацию Nginx
RUN rm /etc/nginx/conf.d/default.conf

# Копируем нашу собственную конфигурацию
COPY nginx.conf /etc/nginx/conf.d/

# Копируем все файлы сайта (html, css, js) в рабочую директорию сервера
COPY . /usr/share/nginx/html

# Указываем, что наше приложение будет работать на порту, который предоставит Railway
EXPOSE 8080

# Команда для запуска сервера
CMD ["nginx", "-g", "daemon off;"]
