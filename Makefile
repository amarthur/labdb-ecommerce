PYTHON := python3
PIP := pip3
NPM := npm

BACK := backend
FRONT := frontend

VENV := $(BACK)/venv
VENV_ACTIVATE = source $(VENV)/bin/activate

run_back:
	($(VENV_ACTIVATE) && $(PYTHON) $(BACK)/api/db_api.py)

run_front:
	(cd $(FRONT) && $(NPM) run serve)

example:
	($(VENV_ACTIVATE) && $(PYTHON) $(BACK)/api/example.py)

setup: venv venv_install npm_install npm_build

venv:
	$(PYTHON) -m venv $(VENV)

venv_install:
	($(VENV_ACTIVATE) && \
	$(PIP) install --upgrade pip && \
	$(PIP) install -r $(BACK)/requirements.txt)

npm_install:
	(cd $(FRONT) && $(NPM) install && $(NPM) audit fix)

npm_build:
	(cd $(FRONT) && $(NPM) run build)

clean:
	rm -rf $(VENV)
	rm -rf $(FRONT)/node_modules
	rm -f $(FRONT)/package-lock.json

drop_all:
	($(VENV_ACTIVATE) && $(PYTHON) $(BACK)/api/drop_all.py)
