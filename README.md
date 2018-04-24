# PyDash.io
A Flask Web-service for visualising Flask-Monitoring-Dashboards

You can view a live deployment of this repository at [pydash.io](http://pydash.io)

## Master branch
Use this branch for weekly deadlines

## Development branch
Push to this branch as soon as you've implemented a feature.

# Running the Flask Back-End

1. Move into the `pydash` folder.
2. Setup your virtual environment using `./start_pipenv.sh`.
3. Make sure you have the latest versions of the dependencies using `pipenv install`.
3. Start up the database using the `./start_database.sh` shell-script.
4. In another tab (or after running above script in the background using `&`), run `flask run --no-reload` to start up the web application on port 5000.

If you get errors stating that some attribute of `database_root` does not exist, you might need to run `flask seed` beforehand, to
ensure that the database is properly initialized and filled with some example data.

(The `./start_pipenv.sh` script sets up `FLASK_APP=pydash.py` and `FLASK_DEBUG=1` for you)

# Building the React.js Front-End

1. Move into the `pydash-front` folder.
2. Run `yarn` to install all dependencies.
3. Run`yarn build` to build the React application and put it at the location where the Flask Back-End application can find it.
