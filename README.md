# PyDash.io

![PyDash on Travis](https://api.travis-ci.org/RUGSoftEng/2018-PyDash.io.svg?branch=development)

A Flask Web-service for visualising Flask-Monitoring-Dashboards

You can view a live deployment of this repository at [pydash.io](http://pydash.io)

## Master branch
Use this branch for weekly deadlines

## Development branch
Push to this branch as soon as you've implemented a feature.

# Installing Dependencies

This app manages its language-version dependencies using the ASDF Version Manager.

More information on how to install this can be found in [./docs/setting-up-virtual-env-using-asdf.md](./docs/setting-up-virtual-env-using-asdf.md)

# Running in Development

### Side-Note: Seeding the database

Before running your application for the first time (and possibly after a lot of changes have occurred in the development version), you will want to re-seed your application, using:

`./build_and_run.sh databasebg seed`

## Running the application as a whole

In this case, running `./build_and_run.sh` is enough. This will install front-end dependencies, build the front-end react application, install back-end dependencies, and then start the back-end (which serves the react app and the API) including the database.

The application can be closed using `Ctrl+C`.

In the event that the database does not properly close, use `killall runzeo`.

## Running only the Flask Back-End+Database

`./build_and_run.sh databasebg backend`

## Building the React.js Front-End

`./build_and_run.sh build`

## Running the React.js Front-End separately for a quick feedback-loop

Ensure that the Flask back-end+database is running using above steps.

In one shell: 
`./build_and_run.sh databasebg server`

In another: 

`./build_and_run.sh frontend`


# Testing

Tests are written using `pytest`, with a couple of plugins:

- `pytest-xdist` is used to spread test running over all available CPU cores.
- `pytest-random-order` is used to randomize the order tests are run in, to prevent unwanted coupling between tests.
- `pytest-cov` is used to show code-line coverage of a test run.
- `pytest-bdd` is used to write feature (integration) tests using the Gherkin specification language.
- `pytest-splinter` is used to run the feature (integration) tests using an automated browser.
- `pytest-flask` and `pytest-localserver` are used to server the Flask-app during testing to the automated browser.

## Running all tests

Tests as a whole can be run by:

`./build_and_run.sh test`

To do this manually:

1. move into the `pydash` folder
2. Setup your virtual environment using `./start_pipenv.sh`.
3. Run `pytest`.

Do note that for the integration tests, you will need the `chromedriver` binary (that can be found in your OS distribution's package manager).

You might also need to install development dependencies. This is done by running `cd pydash && pipenv install --dev && cd ..`


## Running only back-end unit tests

Follow the manual steps as above, but instead of `pytest`, run `pytest -k "not features"`

## Running only feature tests

Follow the manual steps as above, but instead of `pytest`, run `pytest -k "features"`

## Running tests iteratively during development

Follow the manual steps as above, but instead of `pytest`, run `pytest -f`
