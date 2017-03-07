# for reference. Currently not in use.


#!/usr/bin/python

import math
import random
import sys

from functools import wraps
from Queue import Queue
from Queue import Empty as QueueEmptyError
from threading import Thread
from multiprocessing import TimeoutError

import unittest
import timeit
import partA
import partB
import partC

PI = math.pi

# these strings will be different in the testing suite used for grading
GLOBAL_SEEDS = [None, 
  None,
  'abcsadfsMYSTERY_SEED_1',
  'defsafdMYSTERY_SEED_2',
  'ghkdfasMYSTERY_SEED_3',
]

TIME_LIMIT = 5 # seconds

GLOBAL_PARAMETERS = [None,

    # Test Case 1 (from template code)
    {'test_case':         1,
     'target_x':          2.1,
     'target_y':          4.3,
     'target_heading':    0.5,
     'target_period':    34.0,
     'target_speed':      1.5,
     'hunter_x':        -10.0,
     'hunter_y':        -10.0,
     'hunter_heading':    0.0
    },

    # Test Case 2 (from autograder)
    {'test_case':         2,
     'target_x':          5.3,
     'target_y':          6.2,
     'target_heading':    0.0,
     'target_period':    20.0,
     'target_speed':      2.3,
     'hunter_x':         -2.8,
     'hunter_y':        -10.2,
     'hunter_heading':    0.0
    },

    # Test Case 3 (from autograder)
    {'test_case':         3,
     'target_x':         -3.9,
     'target_y':          9.5,
     'target_heading':   -2.09,
     'target_period':    31.0,
     'target_speed':      1.45,
     'hunter_x':         -5.7,
     'hunter_y':          3.2,
     'hunter_heading':    2.0
    },

    # Test Case 4 (from autograder)
    {'test_case':         4,
     'target_x':        -10.2,
     'target_y':        -11.8,
     'target_heading':    0.79,
     'target_period':    13.0,
     'target_speed':      4.8,
     'hunter_x':          0.0,
     'hunter_y':          3.2,
     'hunter_heading':    (2*PI)-1.0
    },

    # Test Case 5 (same parameters as Test Case 4 but going in opposite direction)
    {'test_case':         5,
     'target_x':        -10.2,
     'target_y':        -11.8,
     'target_heading':    0.79,
     'target_period':   -13.0,
     'target_speed':      4.8,
     'hunter_x':          0.0,
     'hunter_y':          3.2,
     'hunter_heading':    (2*PI)-1.0
    }

]

NOT_FOUND = """
Part {}, Test Case {}, did not succeed within {} steps.
"""

# The functions curr_time_millis, handler, and timeout are taken from 
# http://github.com/udacity/artificial-intelligence/blob/master/build-a-game-playing-agent/agent_test.py
# as of January 14, 2016, at 11:55 UTC.
# Copyright 2016 Udacity
# A claim of fair use under the copyright laws of the United States is made for the use
# of this code because:
# - It is a limited excerpt of the code from the file listed above.
# - It serves an auxiliary purpose for the code from the file listed above.
# - The code is being used for a nonprofit, educational purpose.
# - The use does not negatively affect the market for Udacity's product.

def curr_time_millis():
    return 1000 * timeit.default_timer()


def handler(obj, testcase, queue):
    try:
        queue.put((None, testcase(obj)))
    except:
        queue.put((sys.exc_info(), None))


def timeout(time_limit):
    """
    Function decorator for unittest test cases to specify test case timeout.
    It is not safe to access system resources (e.g., files) within test
    cases wrapped by this timer.
    """

    def wrapUnitTest(testcase):

        @wraps(testcase)
        def testWrapper(self):

            queue = Queue()

            try:
                p = Thread(target=handler, args=(self, testcase, queue))
                p.daemon = True
                p.start()
                err, res = queue.get(timeout=time_limit)
                p.join()
                if err:
                    raise err[0], err[1], err[2]
                return res
            except QueueEmptyError:
                raise TimeoutError("Test aborted due to timeout. Test was " +
                    "expected to finish in fewer than {} second(s).".format(time_limit))

        return testWrapper

    return wrapUnitTest


# End Udacity code.


class GenericPartTestCase(unittest.TestCase):

    params = {}
    params['tolerance_ratio'] = 0.02

    def run_test_with_params(self, k):
        params = self.params.copy()
        params.update(GLOBAL_PARAMETERS[k]) # how to make k vary?
        found, steps = params['test_method'](params)
        self.assertTrue(found,
            NOT_FOUND.format(params['part'], params['test_case'], steps))

    @timeout(TIME_LIMIT)
    def test_case1(self):
        self.run_test_with_params(1)

    @timeout(TIME_LIMIT)
    def test_case2(self):
        self.run_test_with_params(2)

    @timeout(TIME_LIMIT)
    def test_case3(self):
        self.run_test_with_params(3)

    @timeout(TIME_LIMIT)
    def test_case4(self):
        self.run_test_with_params(4)

    @timeout(TIME_LIMIT)
    def test_case5(self):
        self.run_test_with_params(5)


class PartATestCase(GenericPartTestCase):
    def setUp(self):
        params = self.params
        params['part'] = 1
        params['method_name'] = 'estimate_next_pos'
        params['max_steps'] = 10
        params['noise_ratio'] = 0.00
        #params['test_method'] = simulate_without_hunter
        #params['student_method'] = studentMain2.estimate_next_pos


class PartBTestCase(GenericPartTestCase):
    def setUp(self):
        params = self.params
        params['part'] = 2
        params['method_name'] = 'estimate_next_pos'
        params['max_steps'] = 1000
        params['noise_ratio'] = 0.05
        #params['test_method'] = simulate_without_hunter
        #params['student_method'] = studentMain2.estimate_next_pos


class PartCTestCase(GenericPartTestCase):
    def setUp(self):
        params = self.params
        params['part'] = 3
        params['method_name'] = 'next_move'
        params['max_steps'] = 1000
        params['noise_ratio'] = 0.05
        params['speed_ratio'] = 2.00
        #params['test_method'] = simulate_with_hunter
        #params['student_method'] = studentMain3.next_move




all_suites = map(lambda x: unittest.TestLoader().loadTestsFromTestCase(x), 
    [PartATestCase, PartBTestCase, PartCTestCase])
all_tests = unittest.TestSuite(all_suites)
unittest.TextTestRunner(verbosity=2).run(all_tests)
