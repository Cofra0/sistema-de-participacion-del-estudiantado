# /bin/bash

echo BEFORE

cd /workspace/django-boilerplate/app
pip install --upgrade pip
pip install -r _requirements/base.txt -r _requirements/develop.txt
pur -r _requirements/base.txt
pur -r _requirements/production.txt

psql -U gitpod -c 'CREATE DATABASE boilerplate;'