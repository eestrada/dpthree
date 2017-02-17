VERBOSITY=-vv
PYVER?=

.PHONY: test package clean

test:
	@ echo
	@ python$(PYVER) --version
	@ echo
	python$(PYVER) ./test_dpthree.py $(VERBOSITY)
	python$(PYVER) ./test_builtin.py $(VERBOSITY)

package:
	@ echo "Not implemented yet..."
	@ exit 1

clean:
	rm -rf __pycache__/
	find . -name "*.py[cod]" -delete
