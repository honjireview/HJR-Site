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

# Указываем Gunicorn, как запускать наше приложение, используя порт от Railway.
CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "app:app"]