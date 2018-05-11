#!/bin/bash

PydashPrint()
{
    echo -e '\e[1m\e[92m[PyDash.io]: \e[0m\e[1m' "$1" '\e[0m'
}

BuildFrontend()
{
    PydashPrint "building frontend..."
    cd pydash-front
    yarn
    yarn build
    cd ..
    PydashPrint "Done!"
}

BuildBackend()
{
    PydashPrint "building backend..."
    cd pydash
    mkdir -p logs
    pipenv install
    cd ..
    PydashPrint "Done!"
}

SeedBackend()
{
    PydashPrint "seeding backend..."
    cd pydash
    mkdir -p logs
    export FLASK_APP=pydash.py
    export FLASK_ENV=development
    rm -f ./zeo_filestorage.fs*
    pipenv run flask seed
    cd ..
    cd ..
    PydashPrint "Done!"
}

RunDatabase()
{
    PydashPrint "Starting database in background..."
    cd pydash
    pipenv run "./start_database.sh" &
    cd ..
    PydashPrint "Done!"
}

RunFlask()
{
    PydashPrint "Finally: Starting flask webservice. Close with Ctrl+C"
    cd pydash
    export FLASK_APP=pydash.py
    export FLASK_ENV=development
    pipenv run flask run --no-reload --host=0.0.0.0
    cd ..
}

RunFrontend()
{
    cd pydash-front
    yarn start
    cd ..
    PydashPrint "Done!"
}

RunTests()
{
    cd pydash
    export FLASK_APP=pydash.py
    export FLASK_ENV=development
    pipenv run pytest
    cd ..
    PydashPrint "Done!"
}


if [ $# -gt 0 ];
then
    for i in "$@";
    do
        if [ $i == "seed" ];
        then
            SeedBackend
        fi
        if [ $i == "build" ];
        then
            BuildFrontend
            BuildBackend
        fi
        if [ $i == "database" ];
        then
            RunDatabase
        fi
        if [ $i == "server" ];
        then
            xdg-open "http://localhost:5000" &
            RunFlask
        fi
        if [ $i == "frontend" ];
        then
            RunFrontend
        fi
        if [ $i == "test" ];
        then
            RunTests
        fi
    done;
    PydashPrint "Done! Goodbye :-)"
else
    ./$0 seed build database server
fi
