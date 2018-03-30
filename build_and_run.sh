#!/bin/sh

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
    export FLASK_APP=pydash.py
    export FLASK_DEBUG=1
    pipenv install
    PydashPrint "Done!"
}


RunDatabase()
{
    PydashPrint "Starting database in background..."
    pipenv run "./start_database.sh &"
    PydashPrint "Done!"
}


RunFlask()
{
    PydashPrint "Finally: Starting flask webservice. Close with Ctrl+C"
    pipenv run "flask run"
}

BuildFrontend
BuildBackend
RunDatabase
xdg-open "http://localhost:5000" &
RunFlask

