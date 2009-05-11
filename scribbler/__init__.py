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
import time
import traceback

import locator

class TestParser(object):
    def __init__(self, tests_dir, pattern="*.py"):
        self.tests_dir = tests_dir
        self.pattern = pattern
        self.tests = {}

    def parse(self):
        tests = []
        for filename in locator.locate(self.pattern, self.tests_dir):
            filedir = dirname(filename)
            filename = splitext(split(filename)[1])[0]
            if re.match("^[a-zA-Z]\w+$", filename):
                sys.path.append(filedir)
                try:
                    mod = __import__('%s' % filename)
                except ImportError, err:
                    raise SyntaxError("Error importing '%s'. Error: %s" % (filename, str(err)))
                sys.path.pop()
                tests.extend(self.load_fixture_from_module(mod))
        self.tests = tests

    def load_fixture_from_module(self, mod):
        fixtures = []
        for key, obj in inspect.getmembers(mod):
            if not inspect.isclass(obj): continue
            fixture = TestFixture()
            fixture.test_case = obj
            for key in dir(obj):
                method = getattr(obj, key)
                if not (inspect.ismethod(method) or inspect.isfunction(method)):
                    continue
                if key.startswith("test_"):
                    fixture.tests.append(method)
                    continue
                if key in ["setUp", "setup", "set_up"]:
                    if fixture.setup is None:
                        fixture.setup = method
                    continue
                if key in ["tearDown", "teardown", "tear_down"]:
                    if fixture.teardown is None:
                        fixture.teardown = method
                    continue
            if fixture.tests:
                fixtures.append(fixture)
        
        return fixtures

class TestRunner(object):
    before_test = None
    test_successful = None
    test_failed = None
    tests_executing = 0

    def __init__(self, test_suite, pattern="*.py", working_threads = 5):
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
            self.tests_executing += 1
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
                    self.test_failed(name, test_method, traceback.format_exc())
                self.results.append(name, TestResult.Failure, unicode(err))
            self.tests_executing -= 1
            self.test_queue.task_done()

    def start_processes(self):
        for i in range(self.working_threads):
            t = Thread(target=self.worker)
            t.setDaemon(True)
            t.start()

    def run(self):
        self.start_processes()

        try:
            time.sleep(0.5)
            while (self.tests_executing > 0):
                time.sleep(0.2)
        except KeyboardInterrupt:
            print "Test Run interrupted by the user..."

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
    
