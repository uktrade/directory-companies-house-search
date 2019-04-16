# directory-companies-house-search

[![code-climate-image]][code-climate]
[![circle-ci-image]][circle-ci]
[![codecov-image]][codecov]
[![gitflow-image]][gitflow]
[![calver-image]][calver]

**Companies House search service - the Department for International Trade (DIT)**

For more information on installation please check the [Developers Onboarding Checklist](https://uktrade.atlassian.net/wiki/spaces/ED/pages/32243946/Developers+onboarding+checklist)

---

## Development

### Installing
    $ git clone https://github.com/uktrade/directory-companies-house-search
    $ cd directory-companies-house-search
    $ virtualenv .venv -p python3.6
    $ source .venv/bin/activate
    $ pip install -r requirements_test.txt
    # Start postgres now before proceeding.
    $ make debug_db
    $ make debug_migrate
    $ make debug_createsuperuser
    $ make debug_manage cmd='import_ch_companies'

### Requirements

[Python 3.6](https://www.python.org/downloads/release/python-368/)
[redis](https://redis.io/)


### Configuration
Secrets such as API keys and environment specific configurations are placed in `conf/.env` - a file that is not added to version control. You will need to create that file locally in order for the project to run.
In order to authenticate with the Companies House API set the `DIRECTORY_CH_SEARCH_COMPANIES_HOUSE_API_KEY` before you run the webserver

## Running the webserver

    $ source .venv/bin/activate
    $ make debug_webserver

    $ make debug_webserver

## Run debug celery beat scheduler
    $ make debug_celery_beat_scheduler


## Helpful links
* [Developers Onboarding Checklist](https://uktrade.atlassian.net/wiki/spaces/ED/pages/32243946/Developers+onboarding+checklist)
* [Gitflow branching](https://uktrade.atlassian.net/wiki/spaces/ED/pages/737182153/Gitflow+and+releases)
* [GDS service standards](https://www.gov.uk/service-manual/service-standard)
* [GDS design principles](https://www.gov.uk/design-principles)

## Related projects:
https://github.com/uktrade?q=directory
https://github.com/uktrade?q=great

[code-climate-image]: https://codeclimate.com/github/uktrade/directory-companies-house-search/badges/issue_count.svg
[code-climate]: https://codeclimate.com/github/uktrade/directory-companies-house-search

[circle-ci-image]: https://circleci.com/gh/uktrade/directory-companies-house-search/tree/master.svg?style=svg
[circle-ci]: https://circleci.com/gh/uktrade/directory-companies-house-search/tree/master

[codecov-image]: https://codecov.io/gh/uktrade/directory-companies-house-search/branch/master/graph/badge.svg
[codecov]: https://codecov.io/gh/uktrade/directory-companies-house-search

[gitflow-image]: https://img.shields.io/badge/Branching%20strategy-gitflow-5FBB1C.svg
[gitflow]: https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow

[calver-image]: https://img.shields.io/badge/Versioning%20strategy-CalVer-5FBB1C.svg
[calver]: https://calver.org
