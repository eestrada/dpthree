#!/usr/bin/env python

# NOTE: in case we use Python 2
from __future__ import (print_function,
                        absolute_import,
                        division)
import os
import sys
import unittest
import argparse

try:
    import xmlrunner
except Exception:
    xmlrunner = None


def parse_args(args=sys.argv):
    parser = argparse.ArgumentParser(description='Run all tests code base')
    parser.add_argument('-l', '--level', action='count', default=0, help='Decide '
                        'what level of tests to run. Supplying this multiple '
                        'times will increase the level accordingly. Defaults '
                        'to %(default)d, the lowest (and fastest) level. Currently unused.')
    parser.add_argument('-v', '--verbose', action='count', default=0, help='Verbose output. '
                        'Supplying this multiple times will increase verbosity. '
                        'This is usually unnecesary; the test suite will print '
                        'information when a test fails, which is usually '
                        'all we care about.')

    return parser.parse_args(args[1:])


def main(args=sys.argv):
    pargs = parse_args(args)
    kwds = vars(pargs)

    abspath = os.path.abspath(__file__)
    topdir = os.path.dirname(abspath)
    dirname = topdir
    print(dirname)
    print("Testing Level: %s" % kwds["level"])

    all_suites = []

    ut_suite = unittest.defaultTestLoader.discover(dirname,
                                                   pattern='test_*.py',
                                                   top_level_dir=topdir)
    all_suites.append(ut_suite)

    if kwds["level"] >= 1:
        it_suite = unittest.defaultTestLoader.discover(dirname,
                                                       pattern='itest_*.py',
                                                       top_level_dir=topdir)
        all_suites.append(it_suite)

    final_suite = unittest.TestSuite(all_suites)
    if xmlrunner is not None:
        with open("./shippable/testresults/results.xml", mode="wb") as output:
            runner = xmlrunner.XMLTestRunner(output=output, verbosity=kwds['verbose'])
            result = runner.run(final_suite)
    else:
        runner = unittest.TextTestRunner(verbosity=kwds['verbose'])
        result = runner.run(final_suite)

    return int(not result.wasSuccessful())


if __name__ == "__main__":
    retval = main(sys.argv)
    sys.exit(retval)
