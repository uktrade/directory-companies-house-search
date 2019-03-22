# directory-companies-house-search

[![circle-ci-image]][circle-ci]
[![codecov-image]][codecov]

**Export Directory Companies House search service**

For more information on installation please check the [Developers Onboarding Checklist](https://uktrade.atlassian.net/wiki/spaces/ED/pages/32243946/Developers+onboarding+checklist)

## Requirements

[Python 3.6](https://www.python.org/downloads/release/python-366/)

[redis](https://redis.io/)


## Local installation

    $ git clone https://github.com/uktrade/directory-companies-house-search
    $ cd directory-companies-house-search
    $ make

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


[circle-ci-image]: https://circleci.com/gh/uktrade/directory-companies-house-search/tree/master.svg?style=svg
[circle-ci]: https://circleci.com/gh/uktrade/directory-companies-house-search/tree/master

[codecov-image]: https://codecov.io/gh/uktrade/directory-companies-house-search/branch/master/graph/badge.svg
[codecov]: https://codecov.io/gh/uktrade/directory-companies-house-search
