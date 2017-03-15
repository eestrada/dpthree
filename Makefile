VERBOSITY=-vv
PYTHON_BIN?=python
PYTHON_VERSION?=
VENV=. _venv/bin/activate;
INSTALL_VENV=python -m pip --quiet install virtualenv
CLEANER_CMD=rm -rf _venv/ __pycache__/ *.pyc  *.pyo  *.pyd

.PHONY: setupdev test test2 test3 coverage shippable_test package clean

setupdev: clean
	- if ! $(INSTALL_VENV); then sudo $(INSTALL_VENV); fi
	- $(PYTHON_BIN)$(PYTHON_VERSION) -m virtualenv _venv
	- $(VENV) pip install unittest-xml-reporting coverage
	mkdir -p ./shippable/testresults
	mkdir -p ./shippable/codecoverage

test:
	@ echo
	@ $(PYTHON_BIN)$(PYTHON_VERSION) --version
	@ echo
	$(VENV) $(PYTHON_BIN)$(PYTHON_VERSION) ./run_tests.py $(VERBOSITY)

test2:
	export PYTHON_VERSION=2 && $(MAKE) setupdev && $(MAKE) test

test3:
	export PYTHON_VERSION=3 && $(MAKE) setupdev && $(MAKE) test

coverage:
	- $(VENV) $(PYTHON_BIN)$(PYTHON_VERSION) -m coverage run --timid --branch --omit="_venv/*" ./run_tests.py $(VERBOSITY)
	$(VENV) $(PYTHON_BIN)$(PYTHON_VERSION) -m coverage xml -o ./shippable/codecoverage/coverage.xml ./run_tests.py

shippable_test: setupdev coverage test

package:
	@ echo "Not implemented yet..."
	@ exit 1

clean:
	- if ! $(CLEANER_CMD); then sudo $(CLEANER_CMD); fi
