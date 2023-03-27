#!/bin/bash

echo "CONNECTING TO BD"
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep .2s
done
echo "DB CONNECTED"

cd ./menuapp
python3 manage.py makemigrations
python3 manage.py makemigrations auth menu
python3 manage.py migrate
# python3 manage.py collectstatic --noinput

python3 manage.py base_configuration

python3 manage.py runserver 0.0.0.0:8000

exec "$@"