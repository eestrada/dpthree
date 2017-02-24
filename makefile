VERBOSITY=-vv
PYVER?=
VENV=source _venv/bin/activate;

.PHONY: test test2 test3 package clean

setupdev: clean
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
	rm -rf __pycache__/ _venv/
	find . -name "*.py[cod]" -delete
