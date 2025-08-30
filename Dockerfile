# Используем официальный образ Python
FROM python:3.12-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл с зависимостями
COPY requirements.txt requirements.txt

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь остальной код приложения
COPY . .

# ИЗМЕНЕНИЕ: Запускаем команду через shell ('sh -c'), чтобы переменная $PORT была правильно обработана
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:$PORT app:app"]