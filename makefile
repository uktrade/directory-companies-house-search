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
	python manage.py migrate --noinput; \
	python manage.py runserver 0.0.0.0:$$PORT

django_webserver:
	$(DJANGO_WEBSERVER)

debug_test_last_failed:
	make debug_test pytest_args='--last-failed'

DEBUG_SET_ENV_VARS := \
	export SECRET_KEY=debug; \
	export SIGNATURE_SECRET=debug; \
	export PORT=8012; \
	export DEBUG=true; \
	export DB_NAME=directory_ch_search_debug; \
	export DB_USER=debug; \
	export DB_PASSWORD=debug; \
	export DATABASE_URL=postgres://debug:debug@localhost:5432/directory_ch_search_debug; \
	export SESSION_COOKIE_DOMAIN=.trade.great; \
	export CSRF_COOKIE_SECURE=false; \
	export SESSION_COOKIE_SECURE=false; \
	export GECKO_API_KEY=gecko; \
	export REDIS_CELERY_URL=redis://127.0.0.1:6379; \
	export REDIS_CACHE_URL=redis://127.0.0.1:6379; \
	export CELERY_BROKER_URL=debug; \
	export CELERY_RESULT_BACKEND=debug; \
	export ELASTICSEARCH_ENDPOINT=localhost; \
	export ELASTICSEARCH_PORT=9200; \
	export ELASTICSEARCH_USE_SSL=false; \
	export ELASTICSEARCH_VERIFY_CERTS=false; \
	export ELASTICSEARCH_AWS_ACCESS_KEY_ID=debug; \
	export ELASTICSEARCH_AWS_SECRET_ACCESS_KEY=debug; \
	export HEALTH_CHECK_TOKEN=debug; \
	export ELASTICSEARCH_PROVIDER=localhost

TEST_SET_ENV_VARS := \
	export COMPANIES_HOUSE_API_KEY=debug

debug_webserver:
	 $(DEBUG_SET_ENV_VARS); $(DJANGO_WEBSERVER); $(DJANGO_MIGRATE_ELASTICSEARCH)

debug_celery_beat_scheduler:
	$(DEBUG_SET_ENV_VARS); celery -A conf beat -l info -S django

debug_celery_worker:
	$(DEBUG_SET_ENV_VARS); celery -A conf worker -l info

DEBUG_CREATE_DB := \
	psql -U postgres -tc "SELECT 1 FROM pg_database WHERE datname = '$$DB_NAME'" | \
	grep -q 1 || psql -U postgres -c "CREATE DATABASE $$DB_NAME"; \
	psql -U postgres -tc "SELECT 1 FROM pg_roles WHERE rolname = '$$DB_USER'" | \
	grep -q 1 || echo "CREATE USER $$DB_USER WITH PASSWORD '$$DB_PASSWORD'; GRANT ALL PRIVILEGES ON DATABASE \"$$DB_NAME\" to $$DB_USER; ALTER USER $$DB_USER CREATEDB" | psql -U postgres

debug_db:
	$(DEBUG_SET_ENV_VARS) && $(DEBUG_CREATE_DB)

debug_migrate:
	$(DEBUG_SET_ENV_VARS) && ./manage.py migrate

debug_createsuperuser:
	$(DEBUG_SET_ENV_VARS) && ./manage.py createsuperuser

debug_pytest:
	$(DEBUG_SET_ENV_VARS) && $(TEST_SET_ENV_VARS) && $(DJANGO_MIGRATE) && $(COLLECT_STATIC) && $(PYTEST)

debug_test:
	$(DEBUG_SET_ENV_VARS) && $(TEST_SET_ENV_VARS) && $(DJANGO_MIGRATE) && $(COLLECT_STATIC) && $(FLAKE8) && $(PYTEST)

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

upgrade_requirements:
	pip-compile --upgrade requirements.in

upgrade_test_requirements:
	pip-compile --upgrade requirements_test.in

compile_requirements:
	pip-compile requirements.in
	pip-compile requirements_test.in

upgrade_all_requirements: upgrade_requirements upgrade_test_requirements

.PHONY: build clean test_requirements debug_webserver debug_db debug_test debug heroku_deploy_dev smoke_tests compile_all_requirements
