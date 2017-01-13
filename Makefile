PYTHON ?= python
PYTEST ?= py.test

all: clean test

clean:
	$(PYTHON) setup.py clean
	rm -rf dist

test:
	$(PYTEST) rtchange && flake8 rtchange
