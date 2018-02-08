build: docker_test

clean:
	-find . -type f -name "*.pyc" -delete
	-find . -type d -name "__pycache__" -delete

test_requirements:
	pip install -r requirements_test.txt

DJANGO_MIGRATE := python manage.py migrate --noinput
FLAKE8 := flake8 . --exclude=migrations,.venv
PYTEST := pytest . --cov=. --capture=no --cov-config=.coveragerc $(pytest_args)
COLLECT_STATIC := python manage.py collectstatic --noinput
CODECOV := \
	if [ "$$CODECOV_REPO_TOKEN" != "" ]; then \
	   codecov --token=$$CODECOV_REPO_TOKEN ;\
	fi

test:
	$(DJANGO_MIGRATE) && $(COLLECT_STATIC) && $(FLAKE8) && $(PYTEST) && $(CODECOV)

DJANGO_WEBSERVER := \
	python manage.py collectstatic --noinput; \
	python manage.py distributed_migrate --noinput; \
	python manage.py runserver 0.0.0.0:$$PORT

django_webserver:
	$(DJANGO_WEBSERVER)

DOCKER_COMPOSE_REMOVE_AND_PULL := docker-compose -f docker-compose.yml -f docker-compose-test.yml rm -f && docker-compose -f docker-compose.yml -f docker-compose-test.yml pull
DOCKER_COMPOSE_CREATE_ENVS := python docker/env_writer.py docker/env.json docker/env-postgres.json
DOCKER_COMPOSE_CREATE_TEST_ENVS := python docker/env_writer.py docker/env.test.json docker/env-postgres.test.json

docker_run:
	$(DOCKER_COMPOSE_CREATE_ENVS) && \
	$(DOCKER_COMPOSE_REMOVE_AND_PULL) && \
	docker-compose up --build

DOCKER_SET_DEBUG_ENV_VARS := \
	export DIRECTORY_CH_SEARCH_PORT=8000; \
	export DIRECTORY_CH_SEARCH_DEBUG=true; \
	export DIRECTORY_CH_SEARCH_SECRET_KEY=debug; \
	export DIRECTORY_CH_SEARCH_SIGNATURE_SECRET=debug; \
	export DIRECTORY_CH_SEARCH_POSTGRES_USER=debug; \
	export DIRECTORY_CH_SEARCH_POSTGRES_PASSWORD=debug; \
	export DIRECTORY_CH_SEARCH_POSTGRES_DB=directory_ch_search_debug; \
	export DIRECTORY_CH_SEARCH_DATABASE_URL=postgres://debug:debug@postgres:5432/directory_ch_search_debug; \
	export DIRECTORY_CH_SEARCH_SESSION_COOKIE_DOMAIN=.trade.great; \
	export DIRECTORY_CH_SEARCH_CSRF_COOKIE_SECURE=false; \
	export DIRECTORY_CH_SEARCH_SESSION_COOKIE_SECURE=false; \
	export DIRECTORY_CH_SEARCH_GECKO_API_KEY=gecko; \
	export DIRECTORY_CH_SEARCH_REDIS_URL=debug; \
	export DIRECTORY_CH_SEARCH_ELASTICSEARCH_ENDPOINT=elasticsearch; \
	export DIRECTORY_CH_SEARCH_ELASTICSEARCH_PORT=9200; \
	export DIRECTORY_CH_SEARCH_ELASTICSEARCH_USE_SSL=false; \
	export DIRECTORY_CH_SEARCH_ELASTICSEARCH_VERIFY_CERTS=false; \
	export DIRECTORY_CH_SEARCH_ELASTICSEARCH_AWS_ACCESS_KEY_ID=debug; \
	export DIRECTORY_CH_SEARCH_ELASTICSEARCH_AWS_SECRET_ACCESS_KEY=debug; \
	export DIRECTORY_CH_SEARCH_HEALTH_CHECK_TOKEN=debug

docker_test_env_files:
	$(DOCKER_SET_DEBUG_ENV_VARS) && \
	$(DOCKER_COMPOSE_CREATE_TEST_ENVS)

DOCKER_REMOVE_ALL := \
	docker ps -a | \
	grep -e directorychsearch_ | \
	awk '{print $$1 }' | \
	xargs -I {} docker rm -f {}

docker_remove_all:
	$(DOCKER_REMOVE_ALL)

docker_debug: docker_remove_all
	$(DOCKER_SET_DEBUG_ENV_VARS) && \
	$(DOCKER_COMPOSE_CREATE_ENVS) && \
	docker-compose pull && \
	docker-compose build && \
	docker-compose run -d --no-deps celery_beat_scheduler && \
	docker-compose run -d --no-deps celery_worker && \
	docker-compose run --service-ports webserver make django_webserver

debug_test_last_failed:
	make debug_test pytest_args='--last-failed'

docker_webserver_bash:
	docker exec -it directorychsearch_webserver_1 sh

docker_psql:
	docker-compose run postgres psql -h postgres -U debug

docker_test: docker_remove_all
	$(DOCKER_SET_DEBUG_ENV_VARS) && \
	$(DOCKER_COMPOSE_CREATE_ENVS) && \
	$(DOCKER_COMPOSE_CREATE_TEST_ENVS) && \
	$(DOCKER_COMPOSE_REMOVE_AND_PULL) && \
	docker-compose -f docker-compose-test.yml build && \
	docker-compose -f docker-compose-test.yml run sut

docker_build:
	docker build -t ukti/directory-ch-search:latest .

DEBUG_SET_ENV_VARS := \
	export SECRET_KEY=debug; \
	export SIGNATURE_SECRET=debug; \
	export PORT=8000; \
	export DEBUG=true; \
	export DB_NAME=directory_ch_search_debug; \
	export DB_USER=debug; \
	export DB_PASSWORD=debug; \
	export DATABASE_URL=postgres://debug:debug@localhost:5432/directory_ch_search_debug; \
	export SESSION_COOKIE_DOMAIN=.trade.great; \
	export CSRF_COOKIE_SECURE=false; \
	export SESSION_COOKIE_SECURE=false; \
	export GECKO_API_KEY=gecko; \
	export REDIS_URL=redis://127.0.0.1:6379; \
	export CELERY_BROKER_URL=debug; \
	export CELERY_RESULT_BACKEND=debug; \
	export ELASTICSEARCH_ENDPOINT=localhost; \
	export ELASTICSEARCH_PORT=9200; \
	export ELASTICSEARCH_USE_SSL=false; \
	export ELASTICSEARCH_VERIFY_CERTS=false; \
	export ELASTICSEARCH_AWS_ACCESS_KEY_ID=debug; \
	export ELASTICSEARCH_AWS_SECRET_ACCESS_KEY=debug; \
	export HEALTH_CHECK_TOKEN=debug

debug_webserver:
	 $(DEBUG_SET_ENV_VARS); $(DJANGO_WEBSERVER); $(DJANGO_MIGRATE_ELASTICSEARCH);

debug_celery_beat_scheduler:
	$(DEBUG_SET_ENV_VARS); export CELERY_ENABLED=true; export CELERY_BROKER_URL=redis://127.0.0.1:6379; export CELERY_RESULT_BACKEND=redis://127.0.0.1:6379; celery -A chsearch beat -l info -S django

debug_celery_worker:
	$(DEBUG_SET_ENV_VARS); export CELERY_ENABLED=true; export CELERY_BROKER_URL=redis://127.0.0.1:6379; export CELERY_RESULT_BACKEND=redis://127.0.0.1:6379; celery -A chsearch worker -l info

DEBUG_CREATE_DB := \
	psql -U postgres -tc "SELECT 1 FROM pg_database WHERE datname = '$$DB_NAME'" | \
	grep -q 1 || psql -U postgres -c "CREATE DATABASE $$DB_NAME"; \
	psql -U postgres -tc "SELECT 1 FROM pg_roles WHERE rolname = '$$DB_USER'" | \
	grep -q 1 || echo "CREATE USER $$DB_USER WITH PASSWORD '$$DB_PASSWORD'; GRANT ALL PRIVILEGES ON DATABASE \"$$DB_NAME\" to $$DB_USER; ALTER USER $$DB_USER CREATEDB" | psql -U postgres

debug_db:
	$(DEBUG_SET_ENV_VARS) && $(DEBUG_CREATE_DB)

debug_pytest:
	$(DEBUG_SET_ENV_VARS) && $(DJANGO_MIGRATE) && $(COLLECT_STATIC) && $(PYTEST)

debug_test:
	$(DEBUG_SET_ENV_VARS) && $(DJANGO_MIGRATE) && $(COLLECT_STATIC) && $(FLAKE8) && $(PYTEST)

debug_manage:
	$(DEBUG_SET_ENV_VARS) && ./manage.py $(cmd)

debug_shell:
	$(DEBUG_SET_ENV_VARS) && ./manage.py shell

dumpdata:
	$(DEBUG_SET_ENV_VARS) $(printf "\033c") && ./manage.py dumpdata contact enrolment user company buyer notifications --indent 4 > fixtures/development.json

loaddata:
	$(DEBUG_SET_ENV_VARS) && ./manage.py loaddata fixtures/development.json

migrations:
	$(DEBUG_SET_ENV_VARS) && ./manage.py makemigrations contact enrolment user company buyer notifications exportopportunity

debug: test_requirements debug_db debug_test

heroku_deploy_dev:
	docker login --email=$$HEROKU_EMAIL --username=$$HEROKU_EMAIL --password=$$HEROKU_API_KEY registry.heroku.com
	docker build -t registry.heroku.com/directory-ch-search-dev/web .
	docker push registry.heroku.com/directory-ch-search-dev/web
	docker build -t registry.heroku.com/directory-ch-search-dev/celery_beat_scheduler -f Dockerfile-celery_beat_scheduler .
	docker push registry.heroku.com/directory-ch-search-dev/celery_beat_scheduler
	docker build -t registry.heroku.com/directory-ch-search-dev/celery_worker -f Dockerfile-celery_worker .
	docker push registry.heroku.com/directory-ch-search-dev/celery_worker

integration_tests:
	cd $(mktemp -d) && \
	git clone https://github.com/uktrade/directory-tests && \
	cd directory-tests && \
	make docker_integration_tests

compile_requirements:
	python3 -m piptools compile requirements.in

compile_test_requirements:
	python3 -m piptools compile requirements_test.in

compile_all_requirements: compile_requirements compile_test_requirements

.PHONY: build docker_run_test clean test_requirements docker_run docker_debug docker_webserver_bash docker_psql docker_test debug_webserver debug_db debug_test debug heroku_deploy_dev smoke_tests compile_all_requirements
