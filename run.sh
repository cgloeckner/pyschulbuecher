#!/bin/bash

VENV_DIR=~/.local/share/pyschulbuecher/venv
VENV_PIP="$VENV_DIR/bin/pip3"
VENV_PY3="$VENV_DIR/bin/python3"

PORT=8001

URL="http://localhost:$PORT"

echo "------------------------------------------------------------"
echo "Checking python virtual environment $VENV_DIR"
if [ ! -d "$VENV_DIR" ]; then
	echo "Creating VENV"
	python3 -m venv $VENV_DIR
fi

if [ ! -f "$VENV_PIP" ]; then
	echo "pip not found at $VENV_PIP"
	exit 1
fi

if [ ! -f "$VENV_PY3" ]; then
	echo "python3 not found at $VENV_PY3"
	exit 1
fi

echo "Done."
echo "------------------------------------------------------------"
echo "Checking python dependencies"
$VENV_PIP install --upgrade pip
$VENV_PIP install -r requirements.txt

echo "------------------------------------------------------------"
echo "Starting web browser on $URL"
xdg-open "$URL" &

echo "------------------------------------------------------------"
echo "Starting web server"
$VENV_PY3 main.py --port=$PORT
