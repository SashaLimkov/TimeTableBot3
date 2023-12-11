# Указывает Docker использовать официальный образ python 3 с dockerhub в качестве базового образа
FROM python:3.10-slim
# Устанавливает переменную окружения, которая гарантирует, что вывод из python будет отправлен прямо в терминал без предварительной буферизации
ENV PYTHONUNBUFFERED 1
# Устанавливает рабочий каталог контейнера — "app"
WORKDIR /app
# Копирует все файлы из нашего локального проекта в контейнер
ADD . /app

# Запускает команду pip install для всех библиотек, перечисленных в requirements.txt
COPY requirements.txt /app/requirements.txt

RUN apt-get update \
    && apt-get install -y gcc

RUN pip install --no-cache-dir -r requirements.txt




