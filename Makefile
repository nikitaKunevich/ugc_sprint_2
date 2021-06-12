.PHONY = help setup test dev clean
.DEFAULT_GOAL := help

build:
	docker-compose build

run:
	docker-compose -f docker-compose.apps.yml build
	docker-compose down
	docker-compose -f docker-compose.apps.yml -f docker-compose.services.yml up -d
	docker-compose logs analytic_api
	docker-compose logs analytic_worker

down:
	docker-compose -f docker-compose.services.yml -f docker-compose.apps.yml down

sweep:
	isort api/src/ etl/src
	black api/src etl/src
	flake8 api/src etl/src

clean:
	docker-compose down -v --remove-orphans

help:
	@echo "available commands: help, build, down, sweep, run, clean"
