VERBOSITY=-vv
PYBIN_WITH_VER?=python2
VENV=. _venv/bin/activate;
INSTALL_VENV=pip --quiet install virtualenv
CLEANER_CMD=rm -rf _venv/ __pycache__/ *.pyc  *.pyo  *.pyd

.PHONY: setupdev test test2 test3 coverage shippable_test package clean

setupdev: clean
	- if ! $(INSTALL_VENV); then sudo $(INSTALL_VENV); fi
	- $(PYBIN_WITH_VER) -m virtualenv _venv
	- $(VENV) pip install unittest-xml-reporting coverage
	mkdir -p ./shippable/testresults
	mkdir -p ./shippable/codecoverage

test:
	@ echo
	@ $(PYBIN_WITH_VER) --version
	@ echo
	$(VENV) $(PYBIN_WITH_VER) ./run_tests.py $(VERBOSITY)

test2:
	export PYBIN_WITH_VER=python2 && $(MAKE) setupdev && $(MAKE) test

test3:
	export PYBIN_WITH_VER=python3 && $(MAKE) setupdev && $(MAKE) test

coverage:
	- $(VENV) $(PYBIN_WITH_VER) -m coverage run --timid --branch --omit="_venv/*" ./run_tests.py $(VERBOSITY)
	$(VENV) $(PYBIN_WITH_VER) -m coverage xml -o ./shippable/codecoverage/coverage.xml ./run_tests.py

shippable_test: setupdev coverage test

package:
	@ echo "Not implemented yet..."
	@ exit 1

clean:
	- if ! $(CLEANER_CMD); then sudo $(CLEANER_CMD); fi
