# syntax=docker/dockerfile:1

FROM tiangolo/uwsgi-nginx-flask:python3.8

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD [ "gunicorn", "--bind", "0.0.0.0:5000", "run_gunicorn:a"]