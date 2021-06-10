.PHONY = help setup test dev clean
.DEFAULT_GOAL := help

build:
	docker-compose build

run:
	docker-compose build
	docker-compose down
	docker-compose up -d --scale etl=0
	bash -c "sleep 60 && make run_etl" &
	docker-compose logs -f analytic_api movie_api analytic_worker

sweep:
	isort api/src/ etl/src
	black api/src etl/src
	flake8 api/src etl/src

run_etl:
	bash -c "curl -XPUT http://localhost:9200/movies -H 'Content-Type: application/json' -d @movie_api/schemas/es.movies.schema.json; \
  	curl -XPUT http://localhost:9200/persons -H 'Content-Type: application/json' -d @movie_api/schemas/es.persons.schema.json; \
    curl -XPUT http://localhost:9200/genres -H 'Content-Type: application/json' -d @movie_api/schemas/es.genres.schema.json"

	docker-compose up -d etl
	docker-compose logs -f etl

clean:
	docker-compose down -v --remove-orphans

# rebuild:
# 	docker-compose build movie_api auth_api

help:
	@echo "available commands: help, dev, setup_demo, sweep, run, clean"