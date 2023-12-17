.DEFAULT_GOAL := show-help

export


.PHONY: deploy
deploy: stop build database makemigrations migrate createsuperuser start 

.PHONY: build
build:
	docker-compose -f docker-compose.yml build

.PHONY: database
database:
	docker-compose -f docker-compose_db.yml up -d

.PHONY: start
start: start/container
	docker exec ecommerce bash -c "chmod u+x docker-entrypoint.sh && ./docker-entrypoint.sh"
	
.PHONY: makemigrations
makemigrations: start/container
	docker exec ecommerce bash -c "python manage.py makemigrations"

.PHONY: migrate
migrate: start/container
	docker exec ecommerce bash -c "python manage.py migrate"

.PHONY: createsuperuser
createsuperuser: start/container
	docker exec ecommerce bash -c "python manage.py createsuperuser"

.PHONY: stop
stop:
	docker-compose -f docker-compose.yml down

.PHONY: start/container
start/container:
	docker-compose -f docker-compose.yml up -d

.PHONY: logs
logs:
	docker-compose logs --follow

