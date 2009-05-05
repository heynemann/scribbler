#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
from os.path import dirname, abspath, join, split, splitext
root_path = abspath(join(dirname(__file__), "../../"))
sys.path.insert(0, root_path)
from Queue import Queue
from threading import Thread
import unittest
import re
import inspect

import locator

class TestParser(object):
    def __init__(self, tests_dir):
        self.tests_dir = tests_dir
        self.tests = {}

    def parse(self):
        tests = []
        for filename in locator.locate("*.py", self.tests_dir):
            filename = splitext(split(filename)[1])[0]
            if re.match("^[a-zA-Z]\w+$", filename):
                sys.path.append(self.tests_dir)
                module = __import__('%s' % filename)
                sys.path.pop()
                tests.extend(self.load_fixture_from_module(module))
        self.tests = tests

    def load_fixture_from_module(self, module):
        fixtures = []
        for name in dir(module):
            obj = getattr(module, name)
            if not inspect.isclass(obj): continue
            fixture = TestFixture()
            fixture.test_case = obj
            for method_name in dir(obj):
                if method_name.startswith("test_"):
                    fixture.tests.append(getattr(obj, method_name))
                if method_name in ["setUp", "setup", "set_up"]:
                    setup = getattr(obj, method_name)
                    fixture.setup = setup
                if method_name in ["tearDown", "teardown", "tear_down"]:
                    teardown = getattr(obj, method_name)
                    fixture.teardown = teardown
            if fixture.tests:
                fixtures.append(fixture)
        
        return fixtures

class TestRunner(object):
    before_test = None
    test_successful = None
    test_failed = None

    def __init__(self, test_suite, working_threads = 5):
        self.test_suite = test_suite
        self.working_threads = int(working_threads)
        self.test_queue = Queue()
        self.results = TestResult()
        for test_fixture in [suite for suite in self.test_suite if suite is not None]:
            setup = test_fixture.setup
            teardown = test_fixture.teardown
            test_case = test_fixture.test_case
            for test in test_fixture.tests: 
                self.test_queue.put((test_case, setup, teardown, test))

    def worker(self):
        while True:
            test_case_type, setup_method, teardown_method, test_method = self.test_queue.get()
            name = test_method.__name__
            try:
                if self.before_test:
                    self.before_test(name, test_method)
                if unittest.TestCase in test_case_type.__bases__:
                    test_case = test_case_type(name)
                else:
                    test_case = test_case_type()
                if setup_method: setup_method(test_case)
                try:
                    result = test_method(test_case)
                finally:
                    if teardown_method: teardown_method(test_case)
                if self.test_successful:
                    self.test_successful(name, test_method)                
                self.results.append(name, TestResult.Success, None)
            except Exception, err:
                if self.test_failed:
                    self.test_failed(name, test_method, unicode(err))                
                self.results.append(name, TestResult.Failure, unicode(err))
            self.test_queue.task_done()

    def start_processes(self):
        for i in range(self.working_threads):
            t = Thread(target=self.worker)
            t.setDaemon(True)
            t.start()

    def run(self):
        self.start_processes()

        self.test_queue.join()

        return self.results

class TestResult(object):
    Success = "SUCCESS"
    Failure = "FAILURE"

    def __init__(self):
        self.results = []

    def append(self, name, test_result, error):
        self.results.append((name, test_result, error))
    
    def get_status(self):
        status = self.Success
        for name, test_result, error in self.results:
            if error:
                status = self.Failure
        return status

class TestFixture(object):
    def __init__(self):
        self.test_case = None
        self.setup = None
        self.teardown = None
        self.tests = []
    
