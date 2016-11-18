FROM ubuntu:16.04

ENV PROJECT_DIR=/var/www/etherscaner \
    GUNICORN_BIND=0.0.0.0:8000 \
    DJANGO_SECRET_KEY='some_secret_key' \
    DJANGO_DEBUG='True' \
    DJANGO_EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend \
    DJANGO_DATABASE_ENGINE='django.db.backends.postgresql' \
    DJANGO_DATABASE_NAME='ethereumscanner' \
    DJANGO_DATABASE_USER='ethereumscanner' \
    DJANGO_DATABASE_PASSWORD='qqqwww121' \
    DJANGO_DATABASE_HOST='localhost' \
    DJANGO_DATABASE_PORT='5432' \
    DJANGO_SITE_DOMAIN="dev"

COPY requirements.txt $PROJECT_DIR/requirements.txt
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
RUN echo "deb http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.2 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-3.2.list
RUN apt-get update \
    && apt-get install -y \
            postgresql-server-dev-9.5 \
            postgresql-contrib \
            build-essential \
            python3-dev \
            python3-pip \
            mongodb-org \
            redis-server \
    && pip3 install -r $PROJECT_DIR/requirements.txt \
    && pip3 install gunicorn


COPY . $PROJECT_DIR

USER postgres
RUN    /etc/init.d/postgresql start &&\
    psql --command "CREATE USER ethereumscanner WITH SUPERUSER PASSWORD 'qqqwww121';" &&\
    createdb -O ethereumscanner ethereumscanner &&\
    /etc/init.d/postgresql status

USER root
RUN mkdir -p /data/db
EXPOSE 8000 27017 5432

CMD  cd $PROJECT_DIR &&\
     mongod --fork --logpath /var/log/mongod.log &&\
     /etc/init.d/postgresql start &&\
     python3 ./manage.py migrate &&\
     gunicorn --bind $GUNICORN_BIND  --log-level debug ethereum_scanner.wsgi #&\
#     celery --app ethereum_scanner worker -l info
