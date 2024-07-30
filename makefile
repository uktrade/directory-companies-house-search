ARGUMENTS = $(filter-out $@,$(MAKECMDGOALS)) $(filter-out --,$(MAKEFLAGS))

clean:
	-find . -type f -name "*.pyc" -delete
	-find . -type d -name "__pycache__" -delete

pytest:
	ENV_FILES='test,dev' pytest $(ARGUMENTS)

# Usage: make pytest_single <path_to_file>::<method_name>
pytest_single:
	ENV_FILES='test,dev' \
	pytest \
	    $(ARGUMENTS)
		--junit-xml=./results/pytest_unit_report.xml \
		--cov-config=.coveragerc \
		--cov-report=html \
		--cov=. \

ENV_FILES?='test,dev'
pytest_codecov:
	ENV_FILES=$(ENV_FILES) \
	pytest \
		--junit-xml=./results/pytest_unit_report.xml \
		--cov-config=.coveragerc \
		--cov-report=html \
		--cov=. \
		--codecov \
		$(ARGUMENTS)

manage:
	ENV_FILES='secrets-do-not-commit,dev' ./manage.py $(ARGUMENTS)

webserver:
	ENV_FILES='secrets-do-not-commit,dev' python manage.py runserver 0.0.0.0:8000 $(ARGUMENTS)

requirements:
	pip-compile requirements.in --allow-unsafe
	pip-compile requirements_test.in --allow-unsafe

install_requirements:
	pip install -r requirements_test.txt

init_secrets:
	cp conf/env/secrets-template conf/env/secrets-do-not-commit
	sed -i -e 's/#DO NOT ADD SECRETS TO THIS FILE//g' conf/env/secrets-do-not-commit

.PHONY: clean pytest manage webserver requirements install_requirements
