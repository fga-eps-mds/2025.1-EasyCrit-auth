FROM python:3.12-alpine

WORKDIR /app

# Instala as dependências de build ANTES de instalar os pacotes Python
RUN apk add --no-cache build-base linux-headers

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

COPY .env .env

EXPOSE ${PORT}