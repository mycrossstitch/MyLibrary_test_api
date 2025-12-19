FROM python:3.10-alpine3.19

# Системные зависимости
RUN apk add --no-cache gcc musl-dev libffi-dev curl unzip openjdk17


# Скачиваем и ставим Allure CLI
RUN mkdir /allure && \
    curl -Lo /allure/allure.zip https://github.com/allure-framework/allure2/releases/download/2.22.2/allure-2.22.2.zip && \
    unzip /allure/allure.zip -d /allure && \
    ln -s /allure/allure-2.22.2/bin/allure /usr/bin/allure

WORKDIR /usr/workspace
ENV PYTHONPATH=/usr/workspace/src

COPY ./requirements.txt /usr/workspace

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Открываем порт
EXPOSE 8000

# Запускаем приложение
CMD ["uvicorn", "my_library.main:app", "--host", "0.0.0.0", "--port", "8000"]