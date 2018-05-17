#!/bin/sh

export FLASK_APP=pydash.py
export FLASK_ENV=development
export MAIL_USERNAME=noreply.pydashtestmail@gmail.com
export MAIL_PASSWORD=verysecurepydashpassword
pipenv shell
