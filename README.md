# PyDash.io
A Flask Web-service for visualising Flask-Monitoring-Dashboards

You can view a live deployment of this repository at [pydash.io](http://pydash.io)

## Master branch
Use this branch for weekly deadlines

## Development branch
Push to this branch as soon as you've implemented a feature.

# Running in Development

## Running the application as a whole

In this case, running `./build_and_run.sh` is enough. This will install front-end dependencies, build the front-end react application, install back-end dependencies, and then start the back-end (which serves the react app and the API) including the database.

The application can be closed using `Ctrl+C`.

In the event that the database does not properly close, use `killall runzeo`.

## Running only the Flask Back-End+Database

1. Move into the `pydash` folder.
2. Setup your virtual environment using `./start_pipenv.sh`.
3. Make sure you have the latest versions of the dependencies using `pipenv install`.
3. Start up the database using the `./start_database.sh` shell-script.
4. In another tab (or after running above script in the background using `&`), run `flask run --no-reload` to start up the web application on port 5000.

If you get errors stating that some attribute of `database_root` does not exist, you might need to run `flask seed` beforehand, to
ensure that the database is properly initialized and filled with some example data.

(The `./start_pipenv.sh` script sets up `FLASK_APP=pydash.py` and `FLASK_DEBUG=1` for you)

## Building the React.js Front-End

1. Move into the `pydash-front` folder.
2. Run `yarn` to install all dependencies.
3. Run`yarn build` to build the React application and put it at the location where the Flask Back-End application can find it.

## Running the React.js Front-End separately for a quick feedback-loop

Ensure that the Flask back-end+database is running using above steps.

1. Move into the `pydash-front` folder.
2. Run `yarn` to install all dependencies.
3. Run`yarn start` to start an interactive session that will auto-rebuild whenever you make a change.

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

1. move into the `pydash` folder
2. Setup your virtual environment using `./start_pipenv.sh`.
3. Run `pytest`.

Do note that for the integration tests, you will need the `chromedriver` binary (that can be found in your OS distribution's package manager).

## Running only back-end unit tests

Follow the steps as above, but instead of `pytest`, run `pytest -k "not features"`

## Running only feature tests

Follow the steps as above, but instead of `pytest`, run `pytest -k "features"`

## Running tests iteratively during development

Follow the steps as above, but instead of `pytest`, run `pytest -f`
