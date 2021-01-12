FROM python:alpine3.8

COPY . /app

WORKDIR /app

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install -r requirements.txt

EXPOSE 5000

CMD python server.py
