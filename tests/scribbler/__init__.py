#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
from os.path import dirname, abspath, join
root_path = abspath(join(dirname(__file__), "../../"))
sys.path.insert(0, root_path)

from Queue import Queue
from threading import Thread

class TestRunner(object):
    Success = "SUCCESS"
    Failure = "FAILURE"

    def __init__(self, test_suite, working_threads = 5):
        self.test_suite = test_suite
        self.working_threads = int(working_threads)
        self.test_queue = Queue()
        self.results = TestResult()
        for item in self.test_suite:
            self.test_queue.put(item)

    def worker(self):
        while True:
            item = self.test_queue.get()
            try:
                result = item()
                self.results.append(self.Success, None)
            except Exception, err:
                self.results.append(self.Failure, unicode(err))
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
    def __init__(self):
        self.results = []
        self.errors = []

    def append(self, test_result, error):
        self.results.append(test_result)
        self.errors.append(error)
