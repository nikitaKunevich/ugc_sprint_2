.PHONY = help setup test dev clean
.DEFAULT_GOAL := help

build:
	docker-compose -f docker-compose.apps.yml build

run:
	docker-compose -f docker-compose.apps.yml build
	docker-compose -f docker-compose.apps.yml -f docker-compose.services.yml down
	docker-compose -f docker-compose.apps.yml -f docker-compose.services.yml up -d

down:
	docker-compose -f docker-compose.services.yml -f docker-compose.apps.yml down

sweep:
	isort api/src/ etl/src
	black api/src etl/src
	flake8 api/src etl/src

check_formatting:
	isort --check-only api/src/ etl/src
	black --check api/src etl/src
	flake8 api/src etl/src

clean:
	docker-compose -f docker-compose.services.yml -f docker-compose.apps.yml -v --remove-orphans

help:
	@echo "available commands: help, build, down, sweep, run, clean, check_formatting"
