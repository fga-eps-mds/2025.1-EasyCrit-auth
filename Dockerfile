ARG PORT
ARG USER
ARG PASSWORD
ARG ENV
ARG DB_PORT
FROM python:3.12-alpine AS base
WORKDIR /app
RUN apk add --no-cache build-base linux-headers
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./app .
EXPOSE ${PORT}

FROM base as dev
ENV PORT=${PORT}
ENV USER=${USER}
ENV PASSWORD=${PASSWORD}
ENV ENV=${ENV}
ENV DB_PORT=${DB_PORT}
CMD fastapi dev main.py --host 0.0.0.0 --port $PORT
