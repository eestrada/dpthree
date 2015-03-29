VERBOSITY=-vv

.PHONY: test package clean

test:
	python2 ./test_dpthree.py $(VERBOSITY)
	python3 ./test_dpthree.py $(VERBOSITY)
