#!/usr/bin/env python
# -*- coding:utf-8 -*-

import unittest
import time

class TestConsole(unittest.TestCase):
    def test_wait_for_3_seconds(self):
        time.sleep(3)
        assert True
    def test_wait_for_2_seconds(self):
        time.sleep(2)
        assert True
    def test_wait_for_1_seconds(self):
        time.sleep(1)
        assert True
    def test_wait_for_FourthOfA_seconds(self):
        time.sleep(0.25)
        assert True
    def test_wait_for_Half_seconds(self):
        time.sleep(0.5)
        assert True
    def test_wait_for_ThirdOfA_seconds(self):
        time.sleep(0.33)
        assert True
