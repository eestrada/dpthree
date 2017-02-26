VERBOSITY=-vv
PYVER?=
VENV=. _venv/bin/activate;
INSTALL_VENV=python -m pip --quiet install virtualenv
CLEANER_CMD=rm -rf _venv/ __pycache__/ *.pyc  *.pyo  *.pyd

.PHONY: setupdev test test2 test3 package clean

setupdev: clean
	- if ! $(INSTALL_VENV); then sudo $(INSTALL_VENV); fi
	- python$(PYVER) -m virtualenv _venv
	- $(VENV) pip install unittest-xml-reporting
	mkdir -p ./shippable/testresults

test: setupdev
	@ echo
	@ python$(PYVER) --version
	@ echo
	$(VENV) python$(PYVER) ./run_tests.py $(VERBOSITY)
	- $(MAKE) clean

test2:
	export PYVER=2 && $(MAKE) test

test3:
	export PYVER=3 && $(MAKE) test

package:
	@ echo "Not implemented yet..."
	@ exit 1

clean:
	- if ! $(CLEANER_CMD); then sudo $(CLEANER_CMD); fi
