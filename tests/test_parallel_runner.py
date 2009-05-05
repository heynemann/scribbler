#!/usr/bin/env python
#-*- coding:utf-8 -*-

import time
from datetime import datetime
import sys
from os.path import dirname, abspath, join
test_path = abspath(dirname(__file__))
root_path = abspath(join(dirname(__file__), "../"))
sys.path.insert(0, root_path)

from scribbler import TestRunner, TestResult, TestParser, TestFixture

class Klass(object):
    pass

def fixture_for(method):
    test_fixture = TestFixture()
    test_fixture.test_case = Klass
    test_fixture.setup = None
    test_fixture.teardown = None
    test_fixture.tests.append(method)
    return test_fixture

def test_run_tests_in_parallel_returns_something():
    def do_nothing(cls):
        pass
        
    test_suite = [fixture_for(do_nothing)]
    runner = TestRunner(test_suite = test_suite, working_threads = 5)
    result = runner.run()
    assert result is not None

def test_run_tests_in_parallel_returns_test_result_class():
    def do_nothing(cls):
        pass
    test_suite = [fixture_for(do_nothing)]
    runner = TestRunner(test_suite = test_suite, working_threads = 5)
    result = runner.run()
    assert isinstance(result, TestResult)

def test_run_tests_in_parallel_returns_success_result_from_the_test_if_it_passes():
    def do_nothing(cls):
        pass
    test_suite = [fixture_for(do_nothing)]
    runner = TestRunner(test_suite = test_suite, working_threads = 5)
    result = runner.run()
    assert result.results is not None
    assert result.results[0][1] == TestResult.Success

def test_run_tests_in_parallel_returns_failure_and_error_message_from_the_test_if_it_fails():
    def do_fail(cls):
        assert True == False, "True can never be False"
    test_suite = [fixture_for(do_fail)]
    runner = TestRunner(test_suite = test_suite, working_threads = 5)
    result = runner.run()
    assert result.results[0][1] == TestResult.Failure
    assert result.results[0][2] == "True can never be False"

def test_running_tests_in_parallel_takes_a_proper_amount_of_time():
    def do_sleep(cls):
        time.sleep(2)
    
    test_fixture = fixture_for(do_sleep)
    test_suite = (test_fixture, test_fixture, test_fixture, test_fixture, test_fixture, test_fixture)
    
    #given 6 tests and 5 working threads the test should take ten seconds
    runner = TestRunner(test_suite = test_suite, working_threads = 5)
    start_date = datetime.now()
    result = runner.run()

    period = datetime.now() - start_date
    if period.seconds <= 3 or period.seconds >= 5:
        raise ValueError("The test should have finished in ~10 seconds and finished in %d." % period.seconds)

def test_running_tests_in_parallel_return_results():
    parser = TestParser(tests_dir = join(test_path, "samples"))

    parser.parse()
    tests = parser.tests

    runner = TestRunner(test_suite = tests, working_threads = 5)
    start_date = datetime.now()
    result = runner.run()
    
    assert len(result.results) == 1
    assert result.results[0][1] == TestResult.Success, \
                        "The result should've been successful but was %s" % ", ".join(result.results[0])
