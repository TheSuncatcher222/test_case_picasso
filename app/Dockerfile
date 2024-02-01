FROM python:3.11-slim

RUN python -m pip install --upgrade pip

RUN pip install gunicorn==20.1.0

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .
