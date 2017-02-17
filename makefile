VERBOSITY=-vv
PYVER?=

.PHONY: test package clean

test:
	@ echo
	@ python$(PYVER) --version
	@ echo
	- ls -lh /usr/lib64/python$(PYVER)
	- ls -lh "/usr/lib64/python*"
	- ls -lh /usr/lib/python$(PYVER)
	- ls -lh "/usr/lib/python*"
	python$(PYVER) ./test_dpthree.py $(VERBOSITY)
	python$(PYVER) ./test_builtin.py $(VERBOSITY)

package:
	@ echo "Not implemented yet..."
	@ exit 1

clean:
	rm -rf __pycache__/
	find . -name "*.py[cod]" -delete
