FROM python:3.11

# Установка ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Установка зависимостей
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода вашего приложения
COPY . /app

# Запуск вашего бота
CMD ["python", "main.py"]
