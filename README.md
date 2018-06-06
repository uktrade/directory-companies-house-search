# directory-companies-house-search

[![code-climate-image]][code-climate]
[![circle-ci-image]][circle-ci]
[![codecov-image]][codecov]
[![gemnasium-image]][gemnasium]

**Export Directory Companies House search service**

For more information on installation please check the [Developers Onboarding Checklist](https://uktrade.atlassian.net/wiki/spaces/ED/pages/32243946/Developers+onboarding+checklist)

## Requirements

[Docker >= 1.10](https://docs.docker.com/engine/installation/)  
[Docker Compose >= 1.8](https://docs.docker.com/compose/install/)

## Local installation

    $ git clone https://github.com/uktrade/directory-companies-house-search
    $ cd directory-companies-house-search
    $ make

## Running with Docker
Requires all host environment variables to be set.

    $ make docker_run

### Run debug webserver in Docker
Provides defaults for all env vars but ``AWS_ACCESS_KEY_ID`` and ``AWS_SECRET_ACCESS_KEY``

    $ make docker_debug

### Run tests in Docker

    $ make docker_test

### Host environment variables for docker-compose
``.env`` files will be automatically created (with ``env_writer.py`` based on ``env.json`` and ``env-postgres.json``) by ``make docker_test``, based on host environment variables with ``DIRECTORY_API_`` prefix.

## Debugging

### Setup debug environment
Requires locally running PostgreSQL (e.g. [Postgres.app](http://postgresapp.com/) for the Mac)

    $ make debug

### Companies House API
In order to authenticate with the Companies House API set the `DIRECTORY_CH_SEARCH_COMPANIES_HOUSE_API_KEY` env vars on your host machine before you run the webserver.

### Run debug webserver

    $ make debug_webserver

### Run debug celery beat scheduler
Requires Redis (e.g. [Install and config Redis on Mac OS X via Homebrew](https://medium.com/@petehouston/install-and-config-redis-on-mac-os-x-via-homebrew-eb8df9a4f298#.v37jynm6p) for the Mac)

    $ make debug_celery_beat_scheduler


### Run debug tests

    $ make debug_test


[code-climate-image]: https://codeclimate.com/github/uktrade/directory-companies-house-search/badges/issue_count.svg
[code-climate]: https://codeclimate.com/github/uktrade/directory-companies-house-search

[circle-ci-image]: https://circleci.com/gh/uktrade/directory-companies-house-search/tree/master.svg?style=svg
[circle-ci]: https://circleci.com/gh/uktrade/directory-companies-house-search/tree/master

[codecov-image]: https://codecov.io/gh/uktrade/directory-companies-house-search/branch/master/graph/badge.svg
[codecov]: https://codecov.io/gh/uktrade/directory-companies-house-search

[gemnasium-image]: https://gemnasium.com/badges/github.com/uktrade/directory-companies-house-search.svg
[gemnasium]: https://gemnasium.com/github.com/uktrade/directory-companies-house-search
