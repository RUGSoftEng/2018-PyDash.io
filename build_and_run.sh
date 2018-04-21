#!/bin/bash

PydashPrint()
{
    echo -e "\e[1m\e[92m[PyDash.io]: \e[0m\e[1m$1\e[0m"
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
    mkdir logs
    export FLASK_APP=pydash.py
    export FLASK_DEBUG=1
    pipenv install
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
    pipenv run "flask run"
}

BuildFrontend
BuildBackend
RunDatabase
xdg-open "http://localhost:5000" &
RunFlask
PydashPrint "Done! Goodbye :-)"
