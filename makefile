VERBOSITY=-vv
PYVER?=

.PHONY: test test2 test3 package clean

test:
	@ echo
	@ python$(PYVER) --version
	@ echo
	python$(PYVER) ./test_dpthree.py $(VERBOSITY)
	python$(PYVER) ./test_builtin.py $(VERBOSITY)

test2:
	export PYVER=2 && $(MAKE) test

test3:
	export PYVER=3 && $(MAKE) test

package:
	@ echo "Not implemented yet..."
	@ exit 1

clean:
	rm -rf __pycache__/
	find . -name "*.py[cod]" -delete
