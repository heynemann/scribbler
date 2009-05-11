#!/usr/bin/env python
# -*- coding: utf-8 -*-

u"""scribbler - BDD Acceptance testing

Example usage
=============

    python scribbler.py

:author: `Bernardo Heynemann <mailto:heynemann@gmail.com>`__
"""

__revision__ = "$Id$"
__docformat__ = 'restructuredtext en'

import os
import sys
import optparse
from os.path import join, dirname, abspath
from scribbler import TestParser, TestRunner, TestResult
import time

def main():
    """ Main function - parses args and runs action """
    parser = optparse.OptionParser(usage="%prog or type %prog -h (--help) for help", description=__doc__, version="%prog" + __revision__)
    parser.add_option("-d", "--dir", dest="dir", default=None, help="Directory to run the tests in. If none specified it runs in the current directory.")
    parser.add_option("-p", "--pattern", dest="pattern", default="*.py", help="Pattern of files to use for retrieving tests.")
    parser.add_option("-r", "--recursive", dest="recursive", default="true", help="Specifies whether sub-folders of the 'dir' parameter should be parsed as well. Defaults to 'true' (set to 'false' to parse only the tests in the specified dir)")
    parser.add_option("-t", "--threads", dest="threads", default="5", help="Number of threads to run tests with [default: %default].")

    (options, args) = parser.parse_args()

    tests_dir = options.dir and abspath(options.dir) or abspath(os.curdir)

    start_time = time.time()

    parser = TestParser(tests_dir=tests_dir, pattern = options.pattern)
    parser.parse()
    
    test_suite = parser.tests
    
    if not test_suite:
        print "No tests found under %s with the %s pattern" % (tests_dir, options.pattern)
        sys.exit(0)
    
    runner = TestRunner(test_suite=test_suite, pattern=options.pattern, working_threads=int(options.threads))
    
    def print_success(name, test):
        sys.stdout.write(".")
        sys.stdout.flush()
    def print_failure(name, test, message):
        sys.stdout.write("F")
        sys.stdout.flush()

    runner.test_successful = print_success
    runner.test_failed = print_failure
        
    results = runner.run()

    print

    print_tests(results)

    print "-" * 80
    print "Test run successful"
    show_time(start_time)
    print "-" * 80

    sys.exit(0)

def print_tests(results):
    print "Tests:"
    print "-" * 80    
    i = 1
    for name, result, error in results.results:
        if error:
            print "%d - %s - %s\n%s\n\n" % (i, result.lower(), name, error)
        else:
            print "%d - %s - %s" % (i, result.lower(), name)        
        i+=1
    print 

def show_time(start_time):
    period = (time.time() - start_time)
    print "%0.2f s" % period
    
if __name__ == "__main__":
    main()

