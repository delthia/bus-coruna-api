FROM python:3.11.4-alpine3.18

COPY requirements.txt /
RUN pip3 install -r /requirements.txt

COPY . /app
WORKDIR /app

ENTRYPOINT ["./gunicorn.sh"]
