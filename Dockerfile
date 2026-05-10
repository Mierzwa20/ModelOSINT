FROM python:3.14.4-slim-trixie

WORKDIR /app/app

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .
EXPOSE 5555