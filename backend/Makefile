PYTHON := python3
PIP := pip3
VENV := venv
VENV_ACTIVATE = source $(VENV)/bin/activate

run:
	($(VENV_ACTIVATE) && $(PYTHON) ./api/db_api.py)

example:
	($(VENV_ACTIVATE) && $(PYTHON) ./api/example.py)

setup: venv install

venv:
	$(PYTHON) -m venv $(VENV)

install:
	($(VENV_ACTIVATE) && \
	$(PIP) install --upgrade pip && \
	$(PIP) install -r requirements.txt)

clean:
	rm -rf $(VENV)
