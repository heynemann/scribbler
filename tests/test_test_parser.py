#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
from os.path import dirname, abspath, join
test_path = abspath(dirname(__file__))
root_path = abspath(join(dirname(__file__), "../"))
sys.path.insert(0, root_path)

from scribbler import TestParser
from samples.sample_test import SampleTest

def test_test_parser_retrieves_something():
    parser = TestParser(tests_dir = join(test_path, "samples"))

    parser.parse()
    tests = parser.tests
    assert tests is not None

def test_test_parser_retrieves_one_test():
    parser = TestParser(tests_dir = join(test_path, "samples"))

    parser.parse()
    tests = parser.tests
    assert len(tests) == 1, "The length should be 1 but was %d" % len(tests)

def test_test_parser_retrieves_sample_test():
    parser = TestParser(tests_dir = join(test_path, "samples"))

    parser.parse()
    tests = parser.tests
    
    assert tests[0].tests[0].__name__ == "test_pass", \
                "The test should be test_pass but it is a %s instead." % \
                tests[0].tests[0].__name__

