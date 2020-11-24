FROM python:3.7.2-stretch

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

RUN chmod 755 docker-entrypoint.sh

ENTRYPOINT ["/app/docker-entrypoint.sh"]