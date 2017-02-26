VERBOSITY=-vv
_PYVER?=
VENV=. _venv/bin/activate;
INSTALL_VENV=python -m pip --quiet install virtualenv
CLEANER_CMD=rm -rf _venv/ __pycache__/ *.pyc  *.pyo  *.pyd

.PHONY: setupdev test test2 test3 coverage shippable_test package clean

setupdev: clean
	- if ! $(INSTALL_VENV); then sudo $(INSTALL_VENV); fi
	- python$(_PYVER) -m virtualenv _venv
	- $(VENV) pip install unittest-xml-reporting coverage
	mkdir -p ./shippable/testresults
	mkdir -p ./shippable/codecoverage

test:
	@ echo
	@ python$(_PYVER) --version
	@ echo
	$(VENV) python$(_PYVER) ./run_tests.py $(VERBOSITY)

test2:
	export _PYVER=2 && $(MAKE) setupdev && $(MAKE) test

test3:
	export _PYVER=3 && $(MAKE) setupdev && $(MAKE) test

coverage:
	$(VENV) python$(_PYVER) -m coverage run --timid --branch --omit="_venv/*" ./run_tests.py $(VERBOSITY)
	$(VENV) python$(_PYVER) -m coverage xml -o ./shippable/codecoverage/coverage.xml ./run_tests.py

shippable_test: setupdev test coverage

package:
	@ echo "Not implemented yet..."
	@ exit 1

clean:
	- if ! $(CLEANER_CMD); then sudo $(CLEANER_CMD); fi
