#!/bin/bash

sleep 10

alembic upgrade head
waitress-serve --host 0.0.0.0 --port 5000 app:app

tail -f /dev/null