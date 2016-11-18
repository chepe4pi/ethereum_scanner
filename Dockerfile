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
RUN echo "deb http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.2 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-3.2.list
RUN apt-get update \
    && apt-get install -y \
            postgresql-server-dev-9.5 \
            build-essential \
            python3-dev \
            mongodb-org \
            redis-server \
    && pip install -r $PROJECT_DIR/requirements.txt


COPY . $PROJECT_DIR

CMD gunicorn --bind $GUNICORN_BIND --log-level debug --access-logfile - --error-logfile - \
             -c dynamis/gunicorn.conf etherscaner.wsgi
