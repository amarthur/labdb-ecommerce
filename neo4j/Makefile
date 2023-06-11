PYTHON := python3

all: copy_data run

run:
	$(PYTHON) neo.py

# Solução temporária.
copy_data:
	sudo cp -rf ./data/ /var/lib/neo4j/import
