FROM python:3.8

ARG LAUNCHED_FROM_DOCKER_COMPOSE=0

WORKDIR /app

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8050

CMD ["gunicorn","-b","0.0.0.0:8050","app:server"]