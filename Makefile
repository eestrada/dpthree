VERBOSITY?=-vv
PYTYPE?=python
PYVER?=2.7
PYBIN_WITH_VER?=python2.7
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

local_test:
	docker run -it --rm \
		--env="PYBIN_WITH_VER=$(PYBIN_WITH_VER)" \
		-v "$(PWD)":/usr/src/myapp \
		-w /usr/src/myapp \
		"$(PYTYPE):$(PYVER)" make shippable_test

local_test2.7:
	export PYTYPE=python PYVER=2.7 PYBIN_WITH_VER=python2.7 \
		&& $(MAKE) local_test

local_test3.3:
	export PYTYPE=python PYVER=3.3 PYBIN_WITH_VER=python3.3 \
		&& $(MAKE) local_test

local_test3.4:
	export PYTYPE=python PYVER=3.4 PYBIN_WITH_VER=python3.4 \
		&& $(MAKE) local_test

local_test3.5:
	export PYTYPE=python PYVER=3.5 PYBIN_WITH_VER=python3.5 \
		&& $(MAKE) local_test

local_test3.6:
	export PYTYPE=python PYVER=3.6 PYBIN_WITH_VER=python3.6 \
		&& $(MAKE) local_test

local_test_pypy2:
	export PYTYPE=pypy PYVER=2 PYBIN_WITH_VER=pypy \
		&& $(MAKE) local_test

local_test_pypy3:
	export PYTYPE=pypy PYVER=3 PYBIN_WITH_VER=pypy3 \
		&& $(MAKE) local_test

local_test_all: local_test2.7 local_test3.3 local_test3.4 local_test3.5 local_test3.6 local_test_pypy2 local_test_pypy3

coverage:
	- $(VENV) $(PYBIN_WITH_VER) -m coverage run --timid --branch --omit="_venv/*" ./run_tests.py $(VERBOSITY)
	$(VENV) $(PYBIN_WITH_VER) -m coverage xml -o ./shippable/codecoverage/coverage.xml ./run_tests.py

shippable_test: setupdev coverage test

package:
	@ echo "Not implemented yet..."
	@ exit 1

clean:
	- if ! $(CLEANER_CMD); then sudo $(CLEANER_CMD); fi
