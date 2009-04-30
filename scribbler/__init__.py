#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
from os.path import join, split, splitext
from Queue import Queue
from threading import Thread
import unittest
from glob import glob
import re
import unittest

class TestParser(object):
    def __init__(self, tests_dir):
        self.tests_dir = tests_dir
        self.tests = {}

    def parse(self):
        tests = []
        loader = unittest.TestLoader()
        for filename in glob(join(self.tests_dir, "*.py")):
            filename = splitext(split(filename)[1])[0]
            if re.match("^[a-zA-Z]\w+$", filename):
                sys.path.append(self.tests_dir)
                module = __import__('%s' % filename)
                sys.path.pop()
                tests.append(loader.loadTestsFromModule(module))
        self.tests = tests

    def get_actions(self):
        tests = {}
        for test in self.tests:
            for test2 in test._tests:
                for case in test2._tests:
                    test_case_name = case.__class__.__name__
                    for item in dir(case):
                        if re.match("test_", item):
                            test_method = getattr(case, item)
                            test_name = item
                            tests["%s.%s" % (test_case_name, test_name)] = unittest.FunctionTestCase(test_method, None, None).run
        return tests

class TestRunner(object):
    before_test = None
    test_successful = None
    test_failed = None

    def __init__(self, test_suite, working_threads = 5):
        self.test_suite = test_suite
        self.working_threads = int(working_threads)
        self.test_queue = Queue()
        self.results = TestResult()
        for k, v in self.test_suite.items():
            self.test_queue.put((k,v))

    def worker(self):
        while True:
            name, test_method = self.test_queue.get()
            try:
                if self.before_test:
                    self.before_test(name, test_method)
                result = test_method()
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
    
