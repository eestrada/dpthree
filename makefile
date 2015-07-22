VERBOSITY=-vv

.PHONY: test package clean

test:
	python3 ./test_dpthree.py $(VERBOSITY)
	python3 ./test_builtin.py $(VERBOSITY)
	@ echo
	@ echo
	@ echo
	python2 ./test_dpthree.py $(VERBOSITY)
	python3 ./test_builtin.py $(VERBOSITY)

package:
	@ echo "Not implemented yet..."
	@ exit 1

clean:
	rm -rf __pycache__/
	find . -name "*.py[cod]" -delete

