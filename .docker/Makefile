# makefile

build:
	docker-compose -f dc-produccion.yml up -d --build --force-recreate --remove-orphans
	docker ps

restart:
	docker restart django_boilerplate
	docker ps

update:
	git submodule update
	git stash
	git pull
	git stash pop

static:
	docker exec django_boilerplate python manage.py collectstatic --no-input

# loaddata:
# 	docker exec django_boilerplate make loaddata

# backup:
# 	docker exec django_boilerplate make backup

media:
	sudo cp -r ../media/* /home/instalar/media/django_boilerplate

migrate:
	docker exec django_boilerplate python manage.py migrate

ssh:
	docker exec -it django_boilerplate bash

deploy:
	make update
	make build
	make migrate
	# make loaddata
	make static
	make media
	make restart

_secret:
	./app/secret.sh

__media:
	sudo cp -r ../media/* /home/instalar/media/django_boilerplate/