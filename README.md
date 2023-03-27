# directory-companies-house-search

[![code-climate-image]][code-climate]
[![circle-ci-image]][circle-ci]
[![codecov-image]][codecov]
[![gitflow-image]][gitflow]
[![calver-image]][calver]

**Companies House search service - the Department for Business and Trade (DBT)**

For more information on installation please check the [Developers Onboarding Checklist](https://uktrade.atlassian.net/wiki/spaces/ED/pages/32243946/Developers+onboarding+checklist)

---

## Development

Read the [Developers Onboarding Checklist](https://uktrade.atlassian.net/wiki/spaces/ED/pages/32243946/Developers+onboarding+checklist)

The back-end framework is Django. The front-end uses minimal Javascript. The motivation for this is for accessibility reasons, to reduce technical complexity, and reduce cross-browser compatibility issues. Therefore most front-end work will be HTML and SASS/CSS development.

We aim to follow [GDS service standards](https://www.gov.uk/service-manual/service-standard) and [GDS design principles](https://www.gov.uk/design-principles).

## Requirements
[Python 3.9.13](https://www.python.org/downloads/release/python-3913/)  
[Redis]( https://redis.io/)

### SASS
We use SASS CSS pre-compiler. If you're doing front-end work your local machine will also need the following dependencies:  
[node](https://nodejs.org/en/download/)  
[SASS](http://sass-lang.com/)

## Running locally

### Installing
    $ git clone https://github.com/uktrade/directory-companies-house-search
    $ cd directory-companies-house-search
    $ python -m venv .venv
    $ source .venv/bin/activate
    $ make install_requirements
    $ make manage migrate
    $ make manage createsuperuser
    $ make manage import_ch_companies

### Configuration

Secrets such as API keys and environment specific configurations are placed in `conf/env/secrets-do-not-commit` - a file that is not added to version control. To create a template secrets file with dummy values run `make secrets`.

### Commands

| Command                       | Description |
| ----------------------------- | ------------|
| make clean                    | Delete pyc files |
| make pytest                   | Run all tests |
| make pytest test_foo.py       | Run all tests in file called test_foo.py |
| make pytest -- --last-failed` | Run the last tests to fail |
| make pytest -- -k foo         | Run the test called foo |
| make pytest -- <foo>          | Run arbitrary pytest command |
| make flake8                   | Run linting |
| make manage <foo>             | Run arbitrary management command |
| make webserver                | Run the development web server |
| make requirements             | Compile the requirements file |
| make install_requirements     | Installed the compile requirements file |
| make css                      | Compile scss to css |
| make secrets                  | Create your secret env var file |

### Configuration
Secrets such as API keys and environment specific configurations are placed in `conf/.env` - a file that is not added to version control. You will need to create that file locally in order for the project to run.
In order to authenticate with the Companies House API set the `DIRECTORY_CH_SEARCH_COMPANIES_HOUSE_API_KEY` before you run the webserver

## Running the webserver
    $ source .venv/bin/activate
    $ make webserver

## API Schema
API schema is available at paths:  
Direct download (yaml) - openapi/  
Swagger UI - openapi/ui/  
Redoc - openapi/ui/redoc/  

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
