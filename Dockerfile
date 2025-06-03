FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc libpq-dev

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

ARG DB_NAME
ARG DB_USER
ARG DB_PASSWORD
ARG DB_HOST

ENV DB_NAME=$DB_NAME \
    DB_USER=$DB_USER \
    DB_PASSWORD=$DB_PASSWORD \
    DB_HOST=$DB_HOST

COPY . /app

ENV PORT=8000
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
