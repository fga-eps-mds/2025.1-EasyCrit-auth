ARG PORT
ARG USER
ARG PASSWORD
ARG DB_NAME
ARG ENV
ARG DB_PORT
ARG SECRET_KEY
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
ENV DB_NAME=${DB_NAME}
ENV ENV=${ENV}
ENV DB_PORT=${DB_PORT}
ENV SECRET_KEY=${SECRET_KEY}
CMD fastapi dev main.py --host 0.0.0.0 --port $PORT
