import sys
sys.path.append(".")
import pprint
import unittest
import logging
import xmlrunner

import SciPassTest
import SimpleBalancerTest
import BalancerOnlyTest
import InlineTest
import SimpleBalancerOnlyTest
import ConfigTest

logging.basicConfig()

if __name__ == '__main__':
    scipasstests = SciPassTest.suite()
    simplebalancertests = SimpleBalancerTest.suite()
    balancer_only_tests = BalancerOnlyTest.suite()
    simple_balancer_only_tests = SimpleBalancerOnlyTest.suite()
    inline_tests = InlineTest.suite()
    config_tests = ConfigTest.suite()
#    suite = unittest.TestSuite([scipasstests, simplebalancertests, balancer_only_tests, inline_tests, simple_balancer_only_tests])
    suite = unittest.TestSuite([config_tests])
    xmlrunner.XMLTestRunner(output='test-reports').run(suite)

