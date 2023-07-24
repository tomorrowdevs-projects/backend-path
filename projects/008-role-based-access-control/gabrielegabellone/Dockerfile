FROM python:3-alpine

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app

RUN flask db init

CMD flask db stamp head; flask db migrate -m "updating db"; flask db upgrade; flask run --host 0.0.0.0 --port 5000