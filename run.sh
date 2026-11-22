#!/bin/bash

GLOBAL_PYTHON=python3.10
VENV_DIR="$HOME/.local/share/pyschulbuecher/venv"
VENV_PIP="$VENV_DIR/bin/pip"
VENV_PY="$VENV_DIR/bin/python"

echo "------------------------------------------------------------"
echo "Checking python virtual environment $VENV_DIR"
if [ ! -d "$VENV_DIR" ]; then
	echo "Creating VENV"
	$GLOBAL_PYTHON -m venv $VENV_DIR
fi

if [ ! -f "$VENV_PIP" ]; then
	echo "pip not found at $VENV_PIP"
	exit 1
fi

if [ ! -f "$VENV_PY" ]; then
	echo "python3 not found at $VENV_PY"
	exit 1
fi

echo "Done."
echo "------------------------------------------------------------"
echo "Checking local LaTeX compiler"
if ! command -v pdflatex >/dev/null 2>&1; then
	export PATH="$HOME/bin:$HOME/.local/bin:$PATH"
	
	if ! command -v pdflatex >/dev/null 2>&1; then
		echo "installing tinytex"
		wget -O /tmp/install-tinytex.sh https://tinytex.yihui.org/install-bin-unix.sh
		sh /tmp/install-tinytex.sh
	fi
fi

echo "Checking LaTeX packages..."
tlmgr install \
	collection-fontsrecommended \
	collection-latexrecommended \
	collection-langgerman \
	amsmath \
	amsfonts \
	mathtools \
	booktabs \
	csquotes \
	biblatex \
	biber \
	babel-german \
	xurl \
	makecell \
	cancel

echo "Done."
echo "------------------------------------------------------------"
echo "Checking python dependencies"
$VENV_PIP install --upgrade pip
$VENV_PIP install -r requirements.txt

echo "------------------------------------------------------------"
echo "Starting web server"
$VENV_PY main.py
