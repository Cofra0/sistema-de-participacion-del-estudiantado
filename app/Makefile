# makefile
SHELL := /bin/bash

bold := $(shell tput bold)
sgr0 := $(shell tput sgr0)

# loaddata:
# 	python manage.py loaddata _backup/backend.json

# backup:
# 	mkdir bkp
# 	python manage.py dumpdata backend --indent 2 > bkp/backend.json
# 	zip _backup/backup.zip bkp/*.json
# 	rm -rf bkp

# dumpdata:
# 	python manage.py dumpdata backend --indent 2 > _backup/backend.json

run:
	make precommit
	python manage.py runserver 0.0.0.0:8000

precommit:
	black --line-length=140 .
	flake8 --ignore E501 --exclude 'core/settings/*' .